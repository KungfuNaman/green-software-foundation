from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.embeddings.bedrock import BedrockEmbeddings
import torch
from transformers import AutoTokenizer, AutoModel
from huggingface_hub import login
from dotenv import load_dotenv
import os
import requests
from tenacity import retry, wait_fixed, stop_after_attempt

load_dotenv()
HF_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

# dim = 384
EMD_MODEL_ID = "sentence-transformers/all-MiniLM-L6-v2"
# dim = 768
# EMD_MODEL_ID = "sentence-transformers/distilbert-base-nli-mean-tokens"

EXT_MODEL_ID = "meta-llama/Llama-2-7b-chat-hf"
# EXT_MODEL_ID = "meta-llama/Llama-2-13b-hf"
# EXT_MODEL_ID = "openai-community/gpt2"


class Embedder:
    def __init__(self):
        # login(token=HF_TOKEN)
        self.api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{EMD_MODEL_ID}"
        self.headers = {"Authorization": f"Bearer {HF_TOKEN}"}

    def embed(self, texts):
        """
        Get embedding from HTTP POST query to hugging face inference api
        :param texts: list of texts, num = n
        :return: embeddings, shape = (n, 384)
        """
        response = requests.post(self.api_url, headers=self.headers, json={"inputs": texts, "options": {"wait_for_model": True}})
        embeddings = response.json()
        return embeddings

    def embed_documents(self, texts):
        return self.embed(texts)

    def embed_query(self, query):
        return self.embed(query)


class Extractor:
    def __init__(self):
        # login(token=HF_TOKEN)
        self.api_url = f"https://api-inference.huggingface.co/models/{EXT_MODEL_ID}"
        self.headers = {"Authorization": f"Bearer {HF_TOKEN}"}

    @retry(wait=wait_fixed(5), stop=stop_after_attempt(10))
    def query(self, payload):
        response = requests.post(self.api_url, headers=self.headers, json=payload)
        return response.json()

    def generate_answer(self, prompt):
        payload = {"inputs": prompt}
        data = self.query(payload)
        return data


if __name__ == "__main__":
    # t = [
    #     "How do I get a replacement Medicare card?",
    #     "How do I get a replacement card?",
    #     ]
    # embedder = Embedder()
    # output = embedder.embed(t)
    # print(output)
    # print('item: ', len(output))
    # print('dimension: ', len(output[0]))
    # print('='*50)

    p = "What is the meaning of life?"
    extractor = Extractor()
    output = extractor.generate_answer(p)
    print('>'*20)
    print(output)
    print('<'*20)
