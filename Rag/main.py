import os
import time
import json
from dotenv import load_dotenv

from populate_database import setup_database, setup_database_after_clearance
from query_data import query_rag, compare_retrieved_items

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


def evaluate_docs_in_bulk(doc_name):
    """Function to execute the whole Rag Pipeline"""

    # ============================================    CONFIG    ============================================

    prompt_id = "P3"  # Choose From: P1, P2, P3, P4, GROUND_TRUTH_PROMPT
    prompt_template_text = prompts_file[prompt_id]
    embedder_name, generator_name = "llama2", "phi3"
    db_collection_name = doc_name + "_" + embedder_name
    retriever_type = "multiquery"  # Choose From: chroma, multiquery, ensemble, bm25, faiss
    retriever_type_lst = ["chroma", "multiquery", "ensemble"]  # For comparing the retrievers

    fi_helper, fo_helper = FileInputHelper(create_doc=True), FileOutputHelper()
    document_path, logger_file_path, combined_path = get_paths(doc_name, prompt_id, generator_name)

    # ============================================    PIPELINE    ================================================

    # Initialize Embedder
    embedder_obj = Embedder(run_local=True, model_name=embedder_name)
    embedder = embedder_obj.get_embedder()

    # Load Database & Document Chunks
    setup_database_start_time = time.time()
    new_doc_embed, db, doc_chunks = setup_database(embedder, document_path, db_collection_name, fi_helper)
    # new_doc_embed, db, doc_chunks = setup_database_after_clearance(embedder, document_path, collection_name, fi_helper)
    setup_database_end_time = time.time()
    setup_db_time = setup_database_end_time - setup_database_start_time if new_doc_embed else "0"

    # Initialize Retriever
    retriever = get_retriever(retriever_type, db, doc_chunks, embedder)

    # Initialize Retriever List
    retriever_lst = []
    for rtype in retriever_type_lst:
        retriever_lst.append( (rtype, get_retriever(rtype, db, doc_chunks, embedder)) )

    # Initialize Generator
    generator = Generator(run_local=True, model_name=generator_name)

    # Load Query File
    query_file_path = "./documentsFromText/" + doc_name + "/ground_truth.json"
    ground_truth = fi_helper.load_json_file(query_file_path)
    truth_length = len(ground_truth)

    # Iterative Querying

    retrieved_rec = {}
    for q_idx in range(truth_length):
        if q_idx > 1:
            break
        q_question = ground_truth[q_idx].get("query", "")
        # ----------     Regular Invoke & Record to CSV     ----------
        # response_info = query_rag(retriever, generator, prompt_template_text, q_question)
        # response_info["query"] = q_question
        # response_info["setup_db_time"] = setup_db_time
        # response_info["logger_file_path"] = logger_file_path
        # fo_helper.append_to_csv(response_info)
        # TODO: ↓ Should Not Use Missing Log In Parser
        # add_parsed_results(logger_file_path, combined_path, prompt_id)
        # ------------------------------------------------------------

        # ----------     For Comparing Retriever Only     --------------------
        retrieved_rec[q_idx] = compare_retrieved_items(retriever_lst, prompt_template_text, q_question)
        retrieved_rec[q_idx]["truth"] = ground_truth[q_idx]["Response"]["Judgement"]
        print("Finished retrieval for ", doc_name, str(q_idx))
    fo_helper.save_retrieved_to_logger(doc_name, retriever_type_lst, retrieved_rec)
    # ------------------------------------------------------------------------


def get_retriever(retriever_type, db, doc_chunks, embedder):
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
        retriever_obj.set_ensemble_weights(0.4, 0.6)
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



def get_paths(doc_name, pid, gen_model, ground_true=True):
    doc_path = "documentsFromText/" + doc_name + "/content.txt" if ground_true else "./documents/" + doc_name + ".pdf"
    log_path = "./Rag/logger/" + gen_model + "_" + pid + "_" + doc_name + ".csv"
    combined_path = "./Rag/logger/" + gen_model + "_" + pid + "_" + doc_name + "_combined.csv"

    return doc_path, log_path, combined_path


def main():
    # documentsFromText=["CloudFare","Cassandra","Airflow","Flink","Hadoop","Kafka","SkyWalking","Spark","TrafficServer"]
    documentsFromText = ["Netflix", "Uber", "Whatsapp", "Dropbox", "Instagram"]
    documentsFromText = ["Uber"]


    for doc_name in documentsFromText:
        evaluate_docs_in_bulk(doc_name)

    # documents=["3"]
    # for doc_name in documents:
    #   evaluate_docs_in_bulk(doc_name)


if __name__ == "__main__":
    main()
