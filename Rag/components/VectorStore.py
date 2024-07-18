import os
from langchain_community.vectorstores import Chroma
import chromadb


class VectorStore:
    def __init__(self, db_type, collection_name, embedder):
        self.db = None
        self.db_path = ""
        if db_type == 'chroma' and collection_name is not None and embedder is not None:
            self.db_path = os.getenv("CHROMA_PATH")
            self.collection_name = collection_name
            self.embedder = embedder
            self.init_chroma(self.collection_name, self.embedder)
        elif db_type == 'faiss':
            self.db_path = os.getenv("FAISS_PATH")
            self.init_faiss()

    def init_chroma(self, collection_name, embedder):
        persistent_client = chromadb.PersistentClient()
        self.db = Chroma(
            persist_directory=self.db_path,
            client=persistent_client,
            collection_name=collection_name,
            embedding_function=embedder,
        )

    def init_faiss(self):
        self.db = None

    def load_vectordb(self):
        return self.db if self.db is not None else print("No DB available")