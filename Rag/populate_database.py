import os
import shutil
import pymupdf4llm
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
import pandas as pd
import torch
from torch.utils.tensorboard import SummaryWriter
from dotenv import load_dotenv

from get_embedding_function import get_embedding_function
from rag_utils import load_chroma_db


load_dotenv()
CHROMA_PATH = os.getenv("CHROMA_PATH")
EMBEDDINGS_LOG_DIR = os.getenv("EMBEDDINGS_LOG_DIR")  # Directory to save TensorBoard logs


def setup_database(document_path, reset: bool, emb_local: bool):
    # Check if the database should be cleared (using the --clear flag).
    if reset:
        clear_database()
        print("✨  Database Cleared")

    # Create (or update) the data store.
    documents = load_documents(document_path)   # list of langchain_Doc(page_content, meta_data)
    chunks = split_documents(documents)         # split to n chunks of langchain_Doc
    success = add_to_chroma(chunks, emb_local)
    # log_embeddings_to_tensorboard()

    return success


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


def add_to_chroma(chunks: list[Document], emb_local: bool):
    # Initialize langchain db
    db = load_chroma_db(emb_local, db_path=CHROMA_PATH)
    # embedder, collection_name = get_embedding_function(run_local=emb_local)
    # persistent_client = chromadb.PersistentClient()
    # db = Chroma(
    #     persist_directory=CHROMA_PATH,
    #     client=persistent_client,
    #     collection_name=collection_name,
    #     embedding_function=embedder,
    # )

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


def dir_name_washing(dir_str):
    dir_str = dir_str.replace("\\\\", "/")
    dir_str = dir_str.replace("\\", "/")
    return dir_str


def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)


def log_embeddings_to_tensorboard(emb_local: bool):
    # Load Chroma database and get embeddings and metadata
    db = load_chroma_db(emb_local, db_path=CHROMA_PATH)
    # embedder, collection_name = get_embedding_function()
    # persistent_client = chromadb.PersistentClient()
    # db = Chroma(
    #     persist_directory=CHROMA_PATH,
    #     client=persistent_client,
    #     collection_name=collection_name,
    #     embedding_function=embedder,
    # )
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
    setup_database("./documents/3.pdf", True, False)

