from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.embeddings.bedrock import BedrockEmbeddings
from hf_model import Embedder


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
