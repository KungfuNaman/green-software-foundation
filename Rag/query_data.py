import os
import time
import json
from langchain.prompts import ChatPromptTemplate

from components.Embedder import Embedder
from components.Retriever import Retriever
from components.FileOutputHelper import FileOutputHelper
from components.Generator import Generator
from populate_database import setup_database


def query_rag(retriever, prompt_template, query_text: str):

    # Context
    search_start_time = time.time()
    retrieved_items = get_retrieved_chunks(retriever, query_text)
    context_text = get_context(retrieved_items)
    search_end_time = time.time()
    search_time = search_end_time - search_start_time
    print("context is taken out : ", search_time, "s")

    # Prompt
    prompt_template = ChatPromptTemplate.from_template(prompt_template)
    prompt = prompt_template.format(context=context_text, question=query_text)
    # print('*'*25, '  prompt  ', '*'*25, flush=True)
    # print(prompt, flush=True)
    # print('*'*25, '  prompt  ', '*'*25, flush=True)
    print("prompt is created")


    # Format the response
    response_info = {
        "context_text": context_text,
        "search_time": search_time,
        # No longer have Similarity Score as retriever interaction changed
        "retrieved_items": retrieved_items
    }

    # retrieved_info = {
    #     "new_prediction": new_retriever,
    #     "retriever_type": retriever_type,
    #     "question": query_text,
    #     "prediction": response_text,
    #     "chroma_chunks": chroma_retrieved_chunk,
    #     "llm_chunks": ensemble_retrieved_chunk
    # }

    return prompt,response_info


def get_context(retrieved_items, seperator="\n\n---\n\n"):
    retrieved_content = []
    for i in retrieved_items:
        retrieved_content.append(i.page_content)
    context_text = seperator.join([doc for doc in retrieved_content])
    return context_text


def get_retrieved_chunks(retriever, query_text):
    retrieved = retriever.invoke(query_text)
    print("Retrieved ", len(retrieved), " chunks in total")
    return retrieved


if __name__ == "__main__":
    embedder_obj = Embedder(run_local=True, model_name="llama2")
    embedder = embedder_obj.get_embedder()

    # doc_path = "documentsFromText/" + "Netflix" + "/content.txt"
    # coll = "test_collection"
    # _, vecdb, doc_chunks = setup_database(embedder=embedder, document_path=doc_path, collection_name=coll)

    # retriever_obj = Retriever(retriever_type="chroma", vectordb=vecdb)
    # retriever1 = retriever_obj.get_retriever()
    # generator1 = Generator(run_local=True, model_name="phi3")

    # with open("Rag/prompts/prompt.json", 'r') as file:
    #     prompts_file = json.load(file)
    # pt = prompts_file["P2"]
    # qt = "Is there any mention of implementing a stateless design?"

    # prompt,response_info1 = query_rag(retriever1, pt, qt)
    # response_info1["query"] = qt
    # response_info1["setup_db_time"] = "0"
    # response_info1["logger_file_path"] = None

    # fo_helper = FileOutputHelper()
    # fo_helper.append_to_csv(response_info1)


