import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from get_embedding_function import get_embedding_function
import pymupdf4llm
from dotenv import load_dotenv

from rag_utils import load_chroma_db
# from rag_utils import log_embeddings_to_tensorboard

os.environ["KMP_DUPLICATE_LIB_OK"] = 'True'
load_dotenv()
CHROMA_PATH = os.getenv("CHROMA_PATH")

def setup_database(ensemble: bool, document_path, reset: bool, emb_local: bool,create_doc: bool,collection_name:str):
    # Check if the database should be cleared (using the --clear flag).
   
    if ensemble:
        documents = load_documents(document_path,create_doc)
        chunks = split_documents(documents)
        ensemble_retriever = create_ensemble_retriever(chunks)
        success = True
        return success, ensemble_retriever


    if reset:
        clear_database(emb_local,collection_name)
        print("✨  Database Cleared")

    # Create (or update) the data store.
    documents = load_documents(document_path,create_doc)   # list of langchain_Doc(page_content, meta_data)
    chunks = split_documents(documents)         # split to n chunks of langchain_Doc
    success = add_to_chroma(chunks, emb_local,collection_name)
    # log_embeddings_to_tensorboard(emb_local)

    return success


def load_documents(document_path,create_doc):
    # Load all PDFs in the DATA_PATH and convert them to markdown with images.
    documents = []
    if(create_doc):
       document=create_own_doc(document_path)
       documents.append(document)

    else:
        md_text = pymupdf4llm.to_markdown(document_path, write_images=True)
        document = Document(page_content=md_text, metadata={"source": document_path})
        documents.append(document)

    return documents


def create_own_doc(document_path):
    with open(document_path, 'r', encoding='utf-8') as file:
        text_content = file.read()
    
        document = Document(page_content=text_content, metadata={"source": document_path})
        return document


def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)


def add_to_chroma(chunks: list[Document], emb_local: bool,collection_name):
    # Initialize langchain db
    db = load_chroma_db(emb_local, collection_name,db_path=CHROMA_PATH)

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
    
def create_ensemble_retriever(chunks: list[Document]):
    bm25_retriever = BM25Retriever.from_texts(
        [chunk.page_content for chunk in chunks], 
        metadatas=[chunk.metadata for chunk in chunks]
    )
    bm25_retriever.k = 2
    
    #embedding = HuggingFaceInferenceAPIEmbeddings(api_key="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", model_name="sentence-transformers/all-MiniLM-l6-v2")
    embedding, collection_name = get_embedding_function("collection_name", True)


    faiss_vectorstore = FAISS.from_texts(
        [chunk.page_content for chunk in chunks], 
        embedding, 
        metadatas=[chunk.metadata for chunk in chunks]
    )

    faiss_retriever = faiss_vectorstore.as_retriever(search_kwargs={"k": 2})

    ensemble_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, faiss_retriever], weights=[0.5, 0.5]
    )
    return ensemble_retriever

def calculate_chunk_ids(chunks):

    # This will create IDs like "data/monopoly.pdf:6:2"
    # Page Source : Page Number : Chunk Index

    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
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


def clear_database(emb_local,collection_name):
    db = load_chroma_db(emb_local, collection_name,db_path=CHROMA_PATH)
    db.delete_collection()
    # if os.path.exists(CHROMA_PATH):
    #     shutil.rmtree(CHROMA_PATH)

if __name__ == "__main__":
    # path=["documentsFromText/Cassandra/content.txt","documentsFromText/Cloudfare/content.txt"]
    # for item in path:
    #     setup_database(item, True, True,True,"collection_name")
    setup_database(True,"documentsFromText/Cassandra/content.txt", True,True,True,"collection_name")
    

