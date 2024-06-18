from populate_database import setup_database
from query_data import query_rag
import time

document_path = "./documents/3.pdf"


def main():
    query_text = "Can you tell me which and how many servers are used?"
    emb_local = True
    extract_local = True

    # set up database
    setup_database_start_time = time.time()
    is_document_embedded = setup_database(document_path, False, emb_local)
    setup_database_end_time = time.time()
    setup_database_time = setup_database_end_time - setup_database_start_time if is_document_embedded else "0"

    # query to model
    query_rag(query_text, setup_database_time, emb_local, extract_local)


if __name__ == "__main__":
    main()
