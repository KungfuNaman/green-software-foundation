import os
import time
import json
import random
from dotenv import load_dotenv

load_dotenv()
from populate_database import setup_database
from query_data import query_rag
from logger.get_track_llm_response import save_retrieved_to_logger

LLM_MODEL = os.getenv("LLM_MODEL")
USE_ENSEMBLE = True
with open("Rag/prompts/prompt.json", 'r') as file:
    prompts = json.load(file)


def evaluate_docs_in_bulk(doc_name,document_path,logger_file_path,combined_path,create_doc,prompt_template):
    """Function to execute the whole Rag Pipeline"""
    emb_local = True
    extract_local = True
    parts = document_path.split('/')
    retriever_type = "mq"

    # Get the last part
    collection_name = parts[-2]+"_"+LLM_MODEL

    # set up database
    setup_database_start_time = time.time()
    ensemble_retriever = None
    if USE_ENSEMBLE:
        is_document_embedded, ensemble_retriever = setup_database(USE_ENSEMBLE,document_path, False, emb_local,create_doc,collection_name)
    else:
        is_document_embedded = setup_database(USE_ENSEMBLE,document_path, False, emb_local,create_doc,collection_name)
    setup_database_end_time = time.time()
    setup_database_time = setup_database_end_time - setup_database_start_time if is_document_embedded else "0"

    # # query to model
    # # Step 1: Read the JSON file
    # with open("./Rag/prompts/queries.json", "r", encoding="utf-8") as file:
    #     data = json.load(file)

    # # Step 2: Extract the 'query' field
    # queries = data.get("queries", [])
    # count = 0
    # for query_obj in queries:
    #     if count == 20:
    #         break
    #     query_text = query_obj.get("query", "")
    #     print("query_text: ", query_text)
    #     query_rag(query_text, setup_database_time, emb_local, extract_local, logger_file_path, collection_name, prompt_template)
    #     print("count: ", count)
    #     add_parsed_results(logger_file_path, combined_path, PROMPT_ID)
    #     count = count+1

    # Open practice truth file
    with open("./documentsFromText/" + doc_name + "/ground_truth.json", "r", encoding="utf-8") as file:
        ground_truth = json.load(file)

    truth_length = len(ground_truth)

    # Record retrieved data
    retrieve_rec = {}
    for q_idx in range(truth_length):
        # if q_idx > 0:
        #     break
        q_question = ground_truth[q_idx].get("query", "")
        retrieved_info = query_rag(
            USE_ENSEMBLE,
            ensemble_retriever,
            q_question,
            setup_database_time,
            emb_local,
            extract_local,
            logger_file_path,
            collection_name,
            prompt_template,
            retriever_type,
            True
        )
        retrieve_rec[q_idx] = retrieved_info
        retrieve_rec[q_idx]["truth"] = ground_truth[q_idx]["Response"]["Judgement"]
        print("Recorded " + doc_name + " " + str(q_idx))

    # Save to logger folder
    save_retrieved_to_logger(
        doc_name,
        "practices_test",
        retrieve_rec
    )


def main():
    PROMPT_ID="P2"
    prompt_template=prompts[PROMPT_ID]
    
    # for documents from text
    # documentsFromText=["CloudFare","Cassandra","Airflow","Flink","Hadoop","Kafka","SkyWalking","Spark","TrafficServer"]
    documentsFromText = ["Netflix", "Uber", "Whatsapp", "Dropbox", "Instagram"]

    for item in documentsFromText:
        doc_path = "documentsFromText/" + item + "/content.txt"
        log_path = "./Rag/logger/" + LLM_MODEL + "_" + PROMPT_ID+"_" + item + ".csv"
        combined_path = "./Rag/logger/" + LLM_MODEL + "_" + PROMPT_ID+"_" + item + "_combined.csv"
        evaluate_docs_in_bulk(item, doc_path, log_path, combined_path, True, prompt_template)
    
    # for documents from pdf
    # documents=["3"]
    # for item in documents:
    #   doc_path="./documents/"+item+".pdf"
    #   log_path="./Rag/logger/"+LLM_MODEL+"_"+PROMPT_ID+"_"+item+ ".csv"
    #   combined_path="./Rag/logger/"+LLM_MODEL+"_"+PROMPT_ID+"_"+item+ "_combined.csv"
    #   evaluate_docs_in_bulk(doc_path,log_path,combined_path,False,prompt_template,PROMPT_ID)


if __name__ == "__main__":
    main()
