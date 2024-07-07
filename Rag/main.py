import time
import json
from dotenv import load_dotenv
import os
load_dotenv()
from populate_database import setup_database
from query_data import query_rag
from parser import add_parsed_results
LLM_MODEL = os.getenv("LLM_MODEL")


def evaluate_docs_in_bulk(document_path,logger_file_path,combined_path,create_doc,prompt_template):
    """Function to execute the whole Rag Pipeline"""
    emb_local = True
    extract_local = True
    parts = document_path.split('/')

    # Get the last part
    collection_name = parts[-2]

    # set up database
    setup_database_start_time = time.time()
    is_document_embedded = setup_database(document_path, False, emb_local,create_doc,collection_name)
    setup_database_end_time = time.time()
    setup_database_time = setup_database_end_time - setup_database_start_time if is_document_embedded else "0"

    # query to model
    # Read the JSON file
    with open("./Rag/prompts/queries.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    # Step 2: Extract the 'query' field
    queries = data.get("queries", [])
    count = 0
    for query_obj in queries:
        # if count==1:
        #     break
        query_text = query_obj.get("query", "")
        print("query_text: ",query_text)
        query_rag(query_text, setup_database_time, emb_local, extract_local,logger_file_path,collection_name,prompt_template)
        print("count: ",count)
        add_parsed_results(logger_file_path,combined_path)
        count=count+1


with open("Rag/prompts/prompt.json", 'r') as file:
    prompts = json.load(file)

def main():
    
    # for documents from text
    documentsFromText=["CloudFare","Cassandra","Airflow","Flink","Hadoop","Kafka","SkyWalking","Spark","TrafficServer"]
    PROMPT_ID="P2"

    prompt_template=prompts[PROMPT_ID]
    for item in documentsFromText:
        doc_path="documentsFromText/"+item+"/content.txt"
        log_path="./Rag/logger/"+LLM_MODEL+"_"+PROMPT_ID+"_"+item+ ".csv"
        combined_path="./Rag/logger/"+LLM_MODEL+"_"+PROMPT_ID+"_"+item+ "_combined.csv"
        evaluate_docs_in_bulk(doc_path,log_path,combined_path,True,prompt_template)
    
    # for documents from pdf
    # documents=["3","2","1"]
    # for item in documents:
    #     doc_path="./documents/"+item+".pdf"
    #     log_path="./Rag/logger/"+LLM_MODEL+"_"+item+ ".csv"
    #     evaluate_docs_in_bulk(doc_path,log_path,False)






if __name__ == "__main__":
    main()
