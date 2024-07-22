from langchain_community.embeddings.ollama import OllamaEmbeddings
from hf_model import Embedder
import os
LLM_MODEL = os.getenv("LLM_MODEL")

def get_embedding_function(collection_name,run_local=False):
    embedder = None
    if run_local:
        model_id = "llama2"
        embedder = OllamaEmbeddings(model=model_id)
        collection_name = collection_name
    else:
        embedder = Embedder()
        model_id = embedder.model
        collection_name = collection_name
    return embedder, collection_name
