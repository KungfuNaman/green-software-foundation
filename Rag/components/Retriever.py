from langchain.retrievers import EnsembleRetriever, MultiQueryRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_community.vectorstores import FAISS
from langchain_community.llms.ollama import Ollama
from langchain_core.prompts.prompt import PromptTemplate


class Retriever:
    def __init__(self, retriever_type, vectordb=None, doc_chunks=None, llm_name=None, ebr1=None, ebr2=None, embedder=None):
        self.retriever_type = retriever_type
        self.retriever = None
        self.retriever_ready = False
        # multiquery
        if retriever_type == 'multiquery' and vectordb is not None and llm_name is not None:
            self.vectordb, self.llm, self.mq_prompt = vectordb, llm_name, self.get_multiquery_prompt()
            self.init_multiquery_retriever(self.vectordb, self.llm, self.mq_prompt)
        # bm25
        elif retriever_type == 'bm25' and doc_chunks is not None:
            self.document = doc_chunks
            self.init_bm25_retriever(self.document)
        # faiss
        elif retriever_type == 'faiss' and doc_chunks is not None and embedder is not None:
            self.document, self.embedder = doc_chunks, embedder
            self.init_faiss_retriever(self.document, self.embedder)
        # chroma
        elif retriever_type == 'chroma' and vectordb is not None:
            self.vectordb = vectordb
            self.init_chroma_retriever(self.vectordb)
        # ensemble
        elif retriever_type == 'ensemble' and ebr1 is not None and ebr2 is not None:
            self.ebr1, self.ebr2 = ebr1, ebr2
            self.init_ensemble_retriever(self.ebr1, self.ebr2)
        else:
            raise ValueError("Invalid arguments")

    def init_multiquery_retriever(self, vectordb, llm, mq_prompt):
        o_model = Ollama(model=llm)
        self.retriever = MultiQueryRetriever.from_llm(
            retriever=vectordb.as_retriever(),
            llm=o_model,
            prompt=mq_prompt
        )
        self.retriever_ready = True

    def init_bm25_retriever(self, document_chunks):
        # word frequency retriever
        self.retriever = BM25Retriever.from_texts(
            [chunk.page_content for chunk in document_chunks],
            metadatas=[chunk.metadata for chunk in document_chunks]
        )
        self.retriever.k = 5
        self.retriever_ready = True

    def init_faiss_retriever(self, document_chunks, embedder):
        faissdb = FAISS.from_texts(
            [chunk.page_content for chunk in document_chunks],
            embedder,
            metadatas=[chunk.metadata for chunk in document_chunks]
        )
        self.retriever = faissdb.as_retriever(search_kwargs={"k": 5})
        self.retriever_ready = True

    def init_chroma_retriever(self, vectordb):
        """
        Other examples to initialize:
        https://api.python.langchain.com/en/latest/vectorstores/
        langchain_community.vectorstores.chroma.Chroma.html#langchain_community.vectorstores.chroma.Chroma.as_retriever
        """
        self.retriever = vectordb.as_retriever(
            search_type="mmr",
            search_kwargs={'k': 5, 'fetch_k': 50}
        )
        self.retriever_ready = True

    def init_ensemble_retriever(self, ebr1, ebr2):
        self.retriever = EnsembleRetriever(
            retrievers=[ebr1, ebr2], weights=[0.5, 0.5]
        )
        self.retriever_ready = True

    def set_bm25_k(self, k: int):
        if self.retriever_type == "bm25":
            self.retriever.k = k
        else:
            raise ValueError("This retriever is not bm25")

    def set_faiss_k(self, k: int):
        if self.retriever_type == "faiss":
            self.retriever.search_kwargs = {"k": k}
        else:
            raise ValueError("This retriever is not faiss")

    def set_ensemble_weights(self, w1: float, w2: float):
        if self.retriever_type == "ensemble":
            self.retriever.weights = [w1, w2]
        else:
            raise ValueError("This retriever is not ensemble")

    @staticmethod
    def get_multiquery_prompt() -> PromptTemplate:
        prompt = PromptTemplate(
            input_variables=["question"],
            template="""You are an AI language model assistant. Your task is 
            to generate 3 different versions of the given user 
            question to retrieve relevant documents from a vector  database. 
            By generating multiple perspectives on the user question, 
            your goal is to help the user overcome some of the limitations 
            of distance-based similarity search. Provide these alternative 
            questions separated by newlines. Original question: {question}""",
        )
        return prompt

    def get_retriever(self):
        return self.retriever if self.retriever_ready else ValueError("Retriever is not initialized yet.")
