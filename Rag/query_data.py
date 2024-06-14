import argparse
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
import time
from get_embedding_function import get_embedding_function

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


def main():
    # Create CLI.
    # parser = argparse.ArgumentParser()
    # parser.add_argument("query_text", type=str, help="The query text.")
    # args = parser.parse_args()
    # query_text = args.query_text
    query_rag("can you tell me the databases details getting used ?")


def query_rag(query_text: str):
    # Prepare the DB.
    embedding_function = get_embedding_function()
    
    start = time.time()

    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    print("data added to db")
    
    # Search the DB.

    start = time.time()

    results = db.similarity_search_with_score(query_text, k=5)
    print("context is taken out")

    end = time.time()
    print("The time of execution of above program is :",
      (end-start) * 10**3, "ms")

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    print("prompt is created")

    start = time.time()

    model = Ollama(model="llama2")
    response_text = model.invoke(prompt)
    print("response is generated")

    end = time.time()
    print("The time of execution of above program is :",
      (end-start) * 10**3, "ms")

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)
    return response_text


if __name__ == "__main__":
    main()