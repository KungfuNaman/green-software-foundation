from hf_model import Embedder
from langchain_community.vectorstores import Chroma
import chromadb
import os
import torch
import pandas as pd
from torch.utils.tensorboard import SummaryWriter
from get_embedding_function import get_embedding_function

CHROMA_PATH = os.getenv("CHROMA_PATH")
EMBEDDINGS_LOG_DIR = os.getenv(
    "EMBEDDINGS_LOG_DIR"
)  # Directory to save TensorBoard logs


def load_chroma_db(emb_locally: bool, db_path=CHROMA_PATH):
    embedder, collection_name = get_embedding_function(run_local=emb_locally)
    persistent_client = chromadb.PersistentClient()
    db = Chroma(
        persist_directory=db_path,
        client=persistent_client,
        collection_name=collection_name,
        embedding_function=embedder,
    )
    return db

def log_embeddings_to_tensorboard(emb_local: bool):
    # Load Chroma database and get embeddings and metadata
    db = load_chroma_db(emb_local, db_path=CHROMA_PATH)
    
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