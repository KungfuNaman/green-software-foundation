import time
from datetime import datetime
import itertools
import pandas as pd
import json
from dotenv import load_dotenv
import os
load_dotenv()
from populate_database import setup_database
from query_data import query_rag
from parser import add_parsed_results
import random
LLM_MODEL = os.getenv("LLM_MODEL")
with open("Rag/prompts/prompt.json", 'r') as file:
    prompts = json.load(file)


def evaluate_docs_in_bulk(document_path,logger_file_path,combined_path,create_doc,prompt_template,PROMPT_ID):
    """Function to execute the whole Rag Pipeline"""
    emb_local = True
    extract_local = True
    parts = document_path.split('/')

    # Get the last part
    collection_name = parts[-2]+"_"+LLM_MODEL

    # set up database
    setup_database_start_time = time.time()
    is_document_embedded = setup_database(document_path, False, emb_local,create_doc,collection_name)
    setup_database_end_time = time.time()
    setup_database_time = setup_database_end_time - setup_database_start_time if is_document_embedded else "0"

    # query to model
    # Step 1: Read the JSON file
    with open("./Rag/prompts/queries.json", "r", encoding="utf-8") as file:
        data = json.load(file)

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

    # Run random 10 queries
    selected_queries = [random.randint(0, 137) for _ in range(5)]
    print("Selected queries: ", selected_queries)
    q_list = data.get("queries", [])
    retrieve_rec = {}
    for q_idx in selected_queries:
        q_dict = q_list[q_idx]
        q_question = q_dict.get("query", "")
        print("query_text: ", q_question)
        response_text, llm_retrieved_chunks, chroma_retrieved_chunk = query_rag(
            q_question,
            setup_database_time,
            emb_local,
            extract_local,
            logger_file_path,
            collection_name,
            prompt_template
        )
        retrieve_rec.get(q_idx, {})
        retrieve_rec[q_idx] = {
            "text": q_question,
            "llm": llm_retrieved_chunks,
            "chroma": chroma_retrieved_chunk,
            "prediction": response_text
        }

    # Save to logger dir
    folder_name = "Rag/logger/" + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    folder_name = folder_name.replace(" ", "-").replace(":", "-")
    os.makedirs(folder_name, exist_ok=True)
    for idx, content_dict in retrieve_rec.items():
        filename = folder_name + "/q" + str(idx) + ".xlsx"
        header = [
            "query_idx",
            "query",
            "Chroma_Retrieved",
            "Llama2_retrieved",
            "prediction",
        ]
        idx_lst = [idx]
        qtext_lst = [content_dict["text"]]
        chroma_lst = content_dict["chroma"]
        llm_lst = content_dict["llm"]
        pred_lst = [content_dict["prediction"]]
        rows = list(itertools.zip_longest(idx_lst, qtext_lst, chroma_lst, llm_lst, pred_lst, fillvalue=""))
        rows = [list(item) for item in rows]
        df = pd.DataFrame(rows, columns=header)
        df.to_excel(filename, index=False)


def main():
    PROMPT_ID="P2"

    prompt_template=prompts[PROMPT_ID]
    
    # for documents from text
    # documentsFromText=["CloudFare","Cassandra","Airflow","Flink","Hadoop","Kafka","SkyWalking","Spark","TrafficServer"]
    documentsFromText=["Netflix"]

    for item in documentsFromText:
        doc_path="documentsFromText/"+item+"/content.txt"
        log_path="./Rag/logger/"+LLM_MODEL+"_"+PROMPT_ID+"_"+item+ ".csv"
        combined_path="./Rag/logger/"+LLM_MODEL+"_"+PROMPT_ID+"_"+item+ "_combined.csv"
        evaluate_docs_in_bulk(doc_path,log_path,combined_path,True,prompt_template,PROMPT_ID)
    
    # for documents from pdf
    # documents=["3"]
    # for item in documents:
    #   doc_path="./documents/"+item+".pdf"
    #   log_path="./Rag/logger/"+LLM_MODEL+"_"+PROMPT_ID+"_"+item+ ".csv"
    #   combined_path="./Rag/logger/"+LLM_MODEL+"_"+PROMPT_ID+"_"+item+ "_combined.csv"
    #   evaluate_docs_in_bulk(doc_path,log_path,combined_path,False,prompt_template,PROMPT_ID)



if __name__ == "__main__":
    main()
