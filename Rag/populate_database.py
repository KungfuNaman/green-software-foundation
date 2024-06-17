import os
import shutil
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from hf_inference_model import Embedder
from langchain_community.vectorstores import Chroma
import pymupdf4llm
import chromadb
import torch
import pandas as pd
from torch.utils.tensorboard import SummaryWriter


from dotenv import load_dotenv

load_dotenv()
CHROMA_PATH = os.getenv("CHROMA_PATH")


def setup_database(document_path, reset=False):
    # Check if the database should be cleared (using the --clear flag).

    if reset:
        print("✨ Clearing Database")
        clear_database()

    # Create (or update) the data store.
    documents = load_documents(document_path)  # list of 17 langchain Document, each element = 1 page
    chunks = split_documents(documents)         # split to 46 chunks of langchain Document

    return add_to_chroma(chunks)


def load_documents(document_path):
    # Load all PDFs in the DATA_PATH and convert them to markdown with images.
    documents = []
    md_text = pymupdf4llm.to_markdown(document_path, write_images=True)
    document = Document(page_content=md_text, metadata={"source": document_path})
    documents.append(document)
    return documents


def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)


def add_to_chroma(chunks: list[Document]):
    embedder = Embedder()
    persistent_client = chromadb.PersistentClient()
    collection = persistent_client.get_or_create_collection("dim384")

    # langchain db
    db = Chroma(
        persist_directory=CHROMA_PATH,
        client=persistent_client,
        collection_name="dim384",
        embedding_function=embedder,
    )

    # Calculate Page IDs.
    chunks_with_ids = calculate_chunk_ids(chunks)

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
        db.persist()
        return True
    else:
        print("✅ No new documents to add")
        return False


def calculate_chunk_ids(chunks):
    # This will create IDs like "data/monopoly.pdf:6:2"
    # Page Source : Page Number : Chunk Index

    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        source = dir_name_washing(source)
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        # If the page ID is the same as the last one, increment the index.
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        # Calculate the chunk ID.
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        # Add it to the page meta-data.
        chunk.metadata["id"] = chunk_id

    return chunks


# TODO: the 3rd one is not working
def dir_name_washing(dir_str):
    dir_str = dir_str.replace(r"\\", "-")
    dir_str = dir_str.replace(r"//", "-")
    dir_str = dir_str.replace("\ ", "-")
    dir_str = dir_str.replace(r"/", "-")
    return dir_str


def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)


if __name__ == "__main__":
    setup_database("./Rag/documents", False)
