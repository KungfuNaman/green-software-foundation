import os
import shutil
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from get_embedding_function import get_embedding_function
from langchain_community.vectorstores import Chroma
import pymupdf4llm
import torch
import pandas as pd
from torch.utils.tensorboard import SummaryWriter

from dotenv import load_dotenv

load_dotenv()

CHROMA_PATH = os.getenv("CHROMA_PATH")
EMBEDDINGS_LOG_DIR = os.getenv(
    "EMBEDDINGS_LOG_DIR"
)  # Directory to save TensorBoard logs


def setup_database(document_path, reset: False):
    # Check if the database should be cleared (using the --clear flag).

    if reset:
        print("✨ Clearing Database")
        clear_database()

    # Create (or update) the data store.
    documents = load_documents(document_path)
    chunks = split_documents(documents)

    success = add_to_chroma(chunks)
    if success:
        log_embeddings_to_tensorboard()

    return True


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
    # Load the existing database.
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=get_embedding_function()
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


def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)


def log_embeddings_to_tensorboard():
    # Load Chroma database and get embeddings and metadata
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=get_embedding_function()
    )
    embeddings = db.get(include=["embeddings", "metadatas"])
    vectors = embeddings["embeddings"]
    metadata = embeddings["metadatas"]

    # Convert metadata to a pandas DataFrame for easier handling
    metadata_df = pd.DataFrame(metadata)

    # Select specific metadata columns for TensorBoard
    columns = ["id", "source"]
    selected_meta = metadata_df[columns]
    selected_meta_list = selected_meta.to_numpy().tolist()

    # Prepare TensorBoard writer
    writer = SummaryWriter(EMBEDDINGS_LOG_DIR)

    # Convert vectors to tensor
    vectors_tensor = torch.tensor(vectors)

    # Set global step and tag
    global_step = 1
    tag = "model1"

    # Define projector config path
    pbconfig = os.path.join(EMBEDDINGS_LOG_DIR, "projector_config.pbtxt")

    # Read existing projector config entries
    def read_pbconfig(path):
        if os.path.exists(path):
            with open(path, "r") as f:
                entries = f.read()
                return entries
        return ""

    old_entries = read_pbconfig(pbconfig)

    # Add embeddings to TensorBoard
    writer.add_embedding(
        vectors_tensor,
        metadata=selected_meta_list,
        global_step=global_step,
        metadata_header=columns,
        tag=tag,
    )

    writer.close()

    # Write new projector config entries
    new_entry = read_pbconfig(pbconfig)
    with open(pbconfig, "w") as f:
        f.write(old_entries + "\n" + new_entry)

    print(f"Embeddings have been logged to TensorBoard at {EMBEDDINGS_LOG_DIR}")


if __name__ == "__main__":
    setup_database("./documents/3.pdf", False)
