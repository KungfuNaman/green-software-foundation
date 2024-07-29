import sys

import os
import time
import json
from dotenv import load_dotenv
import pymupdf4llm


from populate_database import setup_database, setup_database_after_clearance
from query_data import query_rag, compare_retrieved_items, generate_result

# from parser import add_parsed_results
from components.FileInputHelper import FileInputHelper
from components.FileOutputHelper import FileOutputHelper
from components.Embedder import Embedder
from components.Retriever import Retriever
from components.Generator import Generator

load_dotenv()
LLM_MODEL = os.getenv("LLM_MODEL")
with open("Rag/prompts/prompt.json", 'r') as file:
    prompts_file = json.load(file)


def evaluate_docs_in_bulk(document_path):
    """Function to execute the whole Rag Pipeline"""
    doc_name, extension = parse_doc_path(document_path)

    # ============================================    CONFIG    ============================================

    image_extract = True
    prompt_id = "P3"  # Choose From: P1, P2, P3, P4, GROUND_TRUTH_PROMPT

    prompt_template_text = prompts_file[prompt_id]
    embedder_name, generator_name = "llama2", "phi3"
    db_collection_name = doc_name + "_" + embedder_name
    retriever_type = "multiquery"  # Choose From: chroma, multiquery, ensemble, bm25, faiss
    retriever_type_lst = ["chroma", "multiquery", "ensemble"]  # For comparing the retrievers
    alternate_query_file_path = "./Rag/prompts/old_queries.json"  # Query file to use when ground truth is not available

    fi_helper, fo_helper = FileInputHelper(create_doc=True if extension == "txt" else False), FileOutputHelper()
    logger_file_path, combined_path = get_paths(doc_name, prompt_id, generator_name)

    # ============================================    PIPELINE    ================================================
    
    # Initialize Embedder
    embedder = init_embedder(embedder_name=embedder_name)

    # Prepare Database and Chunking
    setup_db_time, db, doc_chunks = prep_db_and_chunking(embedder, document_path, db_collection_name, fi_helper, image_extract)

    # Initialize Retriever 
    retriever, retriever_lst = init_retriever(retriever_type, retriever_type_lst, db, doc_chunks, embedder)

    # Initialize Generator
    generator = Generator(run_local=True, model_name=generator_name)

    # Load Query File
    try:
        query_file_path = "./documentsFromText/" + doc_name + "/ground_truth.json"
        ground_truth = fi_helper.load_json_file(query_file_path)
    except FileNotFoundError:
        print("Using general queries file as do not have a ground truth for this doc.")
        query_file_path = alternate_query_file_path
        ground_truth = fi_helper.load_json_file(query_file_path)["queries"]

    truth_length = len(ground_truth)

    # Iterative Querying
    retrieved_rec = {}
    for q_idx in range(truth_length):
        # if q_idx > 0:
        #     break
        q_question = ground_truth[q_idx].get("query", "")
        # ----------     Regular Invoke & Record to CSV     ----------
        prompt, response_info = query_rag(retriever, prompt_template_text, q_question)
        response_text, response_info = generate_result(generator, prompt, response_info)
        response_info["query"] = q_question
        response_info["setup_db_time"] = setup_db_time
        response_info["logger_file_path"] = logger_file_path
        fo_helper.append_to_csv(response_info)
        # TODO: ↓ Should Not Use Missing Log In Parser
        # add_parsed_results(logger_file_path, combined_path, prompt_id)
        # ------------------------------------------------------------

        # ----------     For Comparing Retrievers Only     ----------
    #     retrieved_rec[q_idx] = compare_retrieved_items(retriever_lst, prompt_template_text, q_question)
    #     retrieved_rec[q_idx]["truth"] = ground_truth[q_idx]["Response"]["Judgement"]
    #     print("Finished retrieval for ", doc_name, str(q_idx))
    # fo_helper.save_retrieved_to_logger(doc_name, retriever_type_lst, retrieved_rec)
    # ---------------------------------------------------------------


def init_embedder(embedder_name):
    """ Initialize the embedder"""
    embedder_obj = Embedder(run_local=True, model_name=embedder_name)
    embedder = embedder_obj.get_embedder()
    return embedder


def prep_db_and_chunking(embedder, document_path, db_collection_name, fi_helper, image_extract):
    """ Load database & document chunks """
    setup_database_start_time = time.time()
    new_doc_embed, db, doc_chunks = setup_database(embedder, document_path, db_collection_name, fi_helper, image_extract)
    # new_doc_embed, db, doc_chunks = setup_database_after_clearance(embedder, document_path, collection_name, fi_helper)
    setup_database_end_time = time.time()
    setup_db_time = setup_database_end_time - setup_database_start_time if new_doc_embed else "0"
    
    return setup_db_time, db, doc_chunks


def init_retriever(retriever_type, retriever_type_lst, db, doc_chunks, embedder):
    """ Initialize retriever & retriever list """
    retriever = get_retriever(retriever_type, db, doc_chunks, embedder)
    retriever_lst = []
    for rtype in retriever_type_lst:
        retriever_lst.append( (rtype, get_retriever(rtype, db, doc_chunks, embedder)) )

    return retriever, retriever_lst


def get_retriever(retriever_type, db, doc_chunks, embedder):
    """ Get retrievers """
    retriever = None
    if retriever_type == "chroma":
        retriever_obj = Retriever(retriever_type=retriever_type, vectordb=db)
        retriever = retriever_obj.get_retriever()
    elif retriever_type == "multiquery":
        llm_name = "llama2"
        retriever_obj = Retriever(retriever_type=retriever_type, vectordb=db, llm_name=llm_name)
        retriever = retriever_obj.get_retriever()
    elif retriever_type == "ensemble":
        r1_obj = Retriever(retriever_type="bm25", doc_chunks=doc_chunks)
        r1 = r1_obj.get_retriever()
        r2_obj = Retriever(retriever_type="faiss", doc_chunks=doc_chunks, embedder=embedder)
        r2 = r2_obj.get_retriever()
        retriever_obj = Retriever(retriever_type=retriever_type, ebr1=r1, ebr2=r2)
        retriever_obj.set_ensemble_weights(0.6, 0.4)
        retriever = retriever_obj.get_retriever()
    elif retriever_type == "bm25":
        retriever_obj = Retriever(retriever_type="bm25", doc_chunks=doc_chunks)
        retriever_obj.set_bm25_k(k=5)
        retriever = retriever_obj.get_retriever()
    elif retriever_type == "faiss":
        retriever_obj = Retriever(retriever_type="faiss", doc_chunks=doc_chunks, embedder=embedder)
        retriever_obj.set_faiss_k(k=5)
        retriever = retriever_obj.get_retriever()
    return retriever


def get_paths(doc_name, pid, gen_model):
    """ Get all paths needed in the pipeline """
    log_path = "./Rag/logger/" + gen_model + "_" + pid + "_" + doc_name + ".csv"
    combined_path = "./Rag/logger/" + gen_model + "_" + pid + "_" + doc_name + "_combined.csv"

    return log_path, combined_path


def parse_doc_path(doc_path):
    """ Parse the document path """
    doc_name = doc_path.split("/")[-1].split(".")[0]
    extension = doc_path.split(".")[-1]
    return doc_name, extension


def main():
    documents = ["./documents/Netflix.pdf", "./documents/2.pdf"]  # specify whole document path(s) here
    for doc in documents:
        evaluate_docs_in_bulk(doc)


if __name__ == "__main__":
    main()
