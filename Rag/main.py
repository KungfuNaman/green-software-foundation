import os
import time
import json
from dotenv import load_dotenv

from populate_database import setup_database, setup_database_after_clearance
from query_data import query_rag
from parser import add_parsed_results
from components.FileInputHelper import FileInputHelper
from components.FileOutputHelper import FileOutputHelper
from components.Embedder import Embedder
from components.Retriever import Retriever
from components.Generator import Generator

load_dotenv()
LLM_MODEL = os.getenv("LLM_MODEL")
with open("Rag/prompts/prompt.json", 'r') as file:
    prompts_file = json.load(file)


def evaluate_docs_in_bulk(doc_name, prompt_id, document_path, logger_file_path, combined_path):
    """Function to execute the whole Rag Pipeline"""

    # ============================================    CONFIG    ============================================

    fi_helper, fo_helper = FileInputHelper(create_doc=True), FileOutputHelper()
    prompt_template = prompts_file[prompt_id]
    embedder_name, generator_name = "llama2", "phi3"
    db_collection_name = doc_name + "_" + embedder_name
    retriever_type = "multiquery"    # Choose From: chroma, multiquery, bm25, faiss, ensemble

    # ============================================    PIPELINE    ================================================

    # Initialize Embedder
    embedder = Embedder(run_local=True, model_name=embedder_name)

    # Load Database, Input Document Chunks
    setup_database_start_time = time.time()
    new_doc_embed, db, doc_chunks = setup_database(embedder, document_path, db_collection_name, fi_helper)
    # new_doc_embed, db, doc_chunks = setup_database_after_clearance(embedder, document_path, collection_name, fi_helper)
    setup_database_end_time = time.time()
    setup_db_time = setup_database_end_time - setup_database_start_time if new_doc_embed else "0"

    # Initialize Retriever
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
        retriever = retriever_obj.get_retriever()

    # Initialize Generator
    generator = Generator(run_local=True, model_name=generator_name)

    # Load Query File
    query_file_path = "./documentsFromText/" + doc_name + "/ground_truth.json"
    ground_truth = fi_helper.load_json_file(query_file_path)
    truth_length = len(ground_truth)

    # Iterative Querying
    retrieve_rec = {}
    for q_idx in range(truth_length):
        # if q_idx > 0:
        #     break
        q_question = ground_truth[q_idx].get("query", "")
        response_info = query_rag(retriever, generator, prompt_template, q_question)
        response_info["query"] = q_question
        response_info["setup_db_time"] = setup_db_time
        response_info["logger_file_path"] = logger_file_path
        fo_helper.append_to_csv(response_info)
        add_parsed_results(logger_file_path, combined_path, prompt_id)


def main():
    PROMPT_ID = "P2"  # Choose From: P1, P2, P3, GROUND_TRUTH_PROMPT

    # for documents from text
    # documentsFromText=["CloudFare","Cassandra","Airflow","Flink","Hadoop","Kafka","SkyWalking","Spark","TrafficServer"]
    documentsFromText = ["Netflix", "Uber", "Whatsapp", "Dropbox", "Instagram"]

    for doc_name in documentsFromText:
        doc_path = "documentsFromText/" + doc_name + "/content.txt"
        log_path = "./Rag/logger/" + LLM_MODEL + "_" + PROMPT_ID+"_" + doc_name + ".csv"
        combined_path = "./Rag/logger/" + LLM_MODEL + "_" + PROMPT_ID+"_" + doc_name + "_combined.csv"
        evaluate_docs_in_bulk(doc_name, PROMPT_ID, doc_path, log_path, combined_path)

    # # for documents from pdf
    # documents = ["3"]
    # for doc_name in documents:
    #     doc_path = "./documents/" + doc_name + ".pdf"
    #     log_path = "./Rag/logger/" + LLM_MODEL + "_" + PROMPT_ID + "_" + doc_name + ".csv"
    #     combined_path = "./Rag/logger/" + LLM_MODEL + "_" + PROMPT_ID + "_" + doc_name + "_combined.csv"
    #     evaluate_docs_in_bulk(doc_name, PROMPT_ID, doc_path, log_path, combined_path)


if __name__ == "__main__":
    main()
