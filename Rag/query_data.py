import os
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
import time
from get_embedding_function import get_embedding_function
from logger.get_track_llm_response import append_to_csv

CHROMA_PATH = os.getenv("CHROMA_PATH")

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


def main():
    query_rag("can you tell me the databases details getting used ?","")


def query_rag(query_text: str,setup_database_time: str):
    # Prepare the DB.
    embedding_function = get_embedding_function()

    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    print("data added to db : ", setup_database_time, "s")

    # Search the DB.

    search_start_time = time.time()

    similarity_results = db.similarity_search_with_score(query_text, k=5)

    search_end_time = time.time()
    search_time = search_end_time - search_start_time

    print("context is taken out : ", search_time, "s")

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in similarity_results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    print("prompt is created")

    response_start_time = time.time()

    model = Ollama(model="llama2")
    response_text = model.invoke(prompt)

    response_end_time = time.time()
    response_time = response_end_time - response_start_time

    print("response is generated : ", response_time, "s")

    sources = [doc.metadata.get("id", None) for doc, _score in similarity_results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)

    append_to_csv(
        query_text, context_text, search_time, response_text, response_time, setup_database_time,similarity_results
    )
    return response_text


if __name__ == "__main__":
    main()