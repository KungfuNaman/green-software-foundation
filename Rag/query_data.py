import os
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
import time
from hf_model import Extractor
from logger.get_track_llm_response import append_to_csv

from rag_utils import load_chroma_db

CHROMA_PATH = os.getenv("CHROMA_PATH")

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question} and then conclude with either "Yes", "No", or "Not Applicable"
"""


def main(emd_local, ext_local):
    query_rag(
        "can you tell me the databases details getting used?",
        "",
        emd_local,
        ext_local
    )


def query_rag(query_text: str, setup_database_time: str, emb_local: bool, ext_local: bool):
    # Prepare the DB.
    db = load_chroma_db(emb_local)
   
    print("data added to db : ", setup_database_time, "s")

    # Search context in DB.
    search_start_time = time.time()
    similarity_results = db.similarity_search_with_score(query_text, k=5)  # [(Document(), sort_of_sim_rate)]
    search_end_time = time.time()
    search_time = search_end_time - search_start_time
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in similarity_results])
    print("context is taken out : ", search_time, "s")

    # Prompt
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    # print('*'*25, '  prompt  ', '*'*25)
    # print(prompt)
    # print('*'*25, '  prompt  ', '*'*25)
    print("prompt is created")

    # Get response from Extractor LLM
    response_start_time = time.time()
    extractor = Extractor(ext_local)
    response_text = extractor.generate_answer(prompt)
    response_end_time = time.time()
    response_time = response_end_time - response_start_time
    print('*'*25, '  response  ', '*'*25)
    print(response_text)
    print('*'*25, '  response  ', '*'*25)
    print("response is generated: ", response_time, "s")

    # Format the response
    sources = [doc.metadata.get("id", None) for doc, _score in similarity_results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    # print(formatted_response)

    append_to_csv(
        query_text, context_text, search_time, response_text, response_time, setup_database_time,similarity_results
    )
    return response_text


if __name__ == "__main__":
    main(True, True)
