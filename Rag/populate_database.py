import os
from langchain.schema.document import Document
from dotenv import load_dotenv

from components.Embedder import Embedder
from components.VectorStore import VectorStore
from components.FileInputHelper import FileInputHelper

os.environ["KMP_DUPLICATE_LIB_OK"] = 'True'
load_dotenv()
CHROMA_PATH = os.getenv("CHROMA_PATH")


def setup_database(embedder, document_path, collection_name: str, fi_helper, image_extract):

    # load & split documents
    documents = fi_helper.load_documents(document_path, image_extract)   # list of langchain_Doc(page_content, meta_data)
    chunks = fi_helper.split_documents(documents)         # split to n chunks of langchain_Doc

    # load / initialize database
    db_obj = VectorStore(db_type="chroma", collection_name=collection_name, embedder=embedder)
    db = db_obj.load_vectordb()

    # save document chunks to db
    new_doc_embed = add_to_chroma(db, chunks)
    return new_doc_embed, db, chunks


def setup_database_after_clearance(embedder, document_path, collection_name: str, fi_helper):
    clear_database(embedder, collection_name)
    new_doc_embed, db, chunks = setup_database(embedder, document_path, collection_name, fi_helper)
    return new_doc_embed, db, chunks


def add_to_chroma(db, chunks: list[Document]):
    # Calculate Page IDs.
    fi_helper = FileInputHelper()
    chunks_with_ids = fi_helper.calculate_chunk_ids(chunks)

    # Add or Update the documents.
    existing_items = db.get(include=[])  # IDs are always included by default
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    # Only add documents that don't exist in the DB.
    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    if len(new_chunks):
        print(f"👉 Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
        return True
    else:
        print("✅ No new documents to add")
        return False


def clear_database(embedder, collection_name):
    db_obj = VectorStore(db_type="chroma", collection_name=collection_name, embedder=embedder)
    db = db_obj.load_vectordb()
    db.delete_collection()
    # if os.path.exists(CHROMA_PATH):
    #     shutil.rmtree(CHROMA_PATH)


if __name__ == "__main__":
    doc_path = "documentsFromText/Netflix/content.txt"
    embedder_obj = Embedder(run_local=True, model_name="llama2")
    embedder1 = embedder_obj.get_embedder()
    fi_helper1 = FileInputHelper(create_doc=True)
    setup_database(embedder1, doc_path, "collection_name", fi_helper1)
    

