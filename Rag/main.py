from populate_database import setup_database
from query_data import query_rag

document_path = "./Rag/documents"
import time


def main():
    query_text = "can you tell me the databases details getting used ?"
    setup_database_start_time = time.time()

    is_document_embedded=setup_database(document_path, False)
    setup_database_end_time = time.time()

    setup_database_time = setup_database_end_time - setup_database_start_time if is_document_embedded else "0"

    query_rag(query_text, setup_database_time)


if __name__ == "__main__":
    main()
