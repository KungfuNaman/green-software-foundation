import os
from langchain_community.embeddings.ollama import OllamaEmbeddings
import requests


class Embedder:
    def __init__(self, run_local=True, model_name=os.getenv("LLM_MODEL")):
        self.embedder = None
        self.model_name = model_name

        if run_local:
            self.init_local_embedder(self.model_name)
        else:
            self.init_remote_embedder()

    def init_local_embedder(self, model_name):
        self.embedder = OllamaEmbeddings(model=model_name, base_url="http://ollama:11434")
        # self.embedder = OllamaEmbeddings(model=model_name)

    def init_remote_embedder(self):
        self.embedder = HFEmbedder()

    def get_embedder(self):
        return self.embedder


class HFEmbedder:
    HF_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

    def __init__(self):
        self.model = "sentence-transformers/all-MiniLM-L6-v2"                       # dim = 384
        # self.model = "sentence-transformers/distilbert-base-nli-mean-tokens"      # dim = 768
        self.api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{self.model}"
        self.headers = {"Authorization": f"Bearer {HFEmbedder.HF_TOKEN}"}
        self.wait = False

    def embed(self, texts):
        """
        Get embedding from HTTP POST query to hugging face inference api
        :param texts: list of texts, num = n
        :return: embeddings, shape = (n, 384)
        """
        response = requests.post(
            self.api_url,
            headers=self.headers,
            json={"inputs": texts, "options": {"wait_for_model": self.wait}}
        )
        embeddings = response.json()
        return embeddings

    def embed_documents(self, text):
        return self.embed(text)

    def embed_query(self, query):
        return self.embed(query)