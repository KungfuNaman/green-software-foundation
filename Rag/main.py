import time
import json

from populate_database import setup_database
from query_data import query_rag

DOCUMENT_PATH = "./documents/3.pdf"


def main():
    """Function to execute the whole Rag Pipeline"""
    emb_local = True
    extract_local = True

    # set up database
    setup_database_start_time = time.time()
    is_document_embedded = setup_database(DOCUMENT_PATH, False, emb_local)
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
        if count==1:
            break
        query_text = query_obj.get("query", "")
        print("query_text: ",query_text)
        query_rag(query_text, setup_database_time, emb_local, extract_local)

        count=count+1


if __name__ == "__main__":
    main()
