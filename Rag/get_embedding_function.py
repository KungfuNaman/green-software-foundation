from langchain_community.embeddings.ollama import OllamaEmbeddings
from hf_model import Embedder
import os
LLM_MODEL = os.getenv("LLM_MODEL")

def get_embedding_function(run_local=False):
    embedder, collection_name = None, None
    if run_local:
        model_id = LLM_MODEL
        embedder = OllamaEmbeddings(model=model_id)
        collection_name = "local"
    else:
        embedder = Embedder()
        model_id = embedder.model
        collection_name = "remote"
    return embedder, collection_name
