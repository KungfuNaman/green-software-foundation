from langchain_community.embeddings.ollama import OllamaEmbeddings
from hf_model import Embedder
from langchain_community.vectorstores import Chroma
import chromadb
import os

CHROMA_PATH = os.getenv("CHROMA_PATH")


def get_embedding_function(run_local=False):
    embedder, collection_name = None, None
    if run_local:
        # embeddings = BedrockEmbeddings(
        #     credentials_profile_name="default", region_name="us-east-1"
        # )
        model_id = "llama2"
        embedder = OllamaEmbeddings(model=model_id)
        collection_name = "local"
    else:
        embedder = Embedder()
        model_id = embedder.model
        collection_name = "remote"
    return embedder, collection_name


def load_chroma_db(emb_locally: bool, db_path=CHROMA_PATH):
    embedder, collection_name = get_embedding_function(run_local=emb_locally)
    persistent_client = chromadb.PersistentClient()
    # collection = persistent_client.get_or_create_collection(collection_name)
    db = Chroma(
        persist_directory=db_path,
        client=persistent_client,
        collection_name=collection_name,
        embedding_function=embedder,
    )
    return db
