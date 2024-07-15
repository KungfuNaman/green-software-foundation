import os
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
import time
import json
from hf_model import Extractor
from logger.get_track_llm_response import append_to_csv
from rag_utils import load_chroma_db, get_llm_retriever

CHROMA_PATH = os.getenv("CHROMA_PATH")

with open("Rag/prompts/prompt.json", 'r') as file:
    prompts = json.load(file)


def main(emd_local, ext_local):
    PROMPT_ID = "P2"
    prompt_template = prompts[PROMPT_ID]

    query_rag(
        "can you tell me the databases details getting used?", "", emd_local, ext_local,"logger.csv","collection_name","template", "mq"
    )


def query_rag(
    query_text: str, setup_database_time: str, emb_local: bool, ext_local: bool, logger_file_path: str,collection_name, prompt_template, retriever_type, new_retriever
):
    # Prepare the DB.
    db = load_chroma_db(emb_local, collection_name)
    print("data added to db : ", setup_database_time, "s")

    # Prepare Retriever
    retriever = get_llm_retriever(db, retriever_type)
    retrieved_content = retriever.invoke(query_text)
    llm_retrieved_chunk = []
    print("LLM retrieved ", len(retrieved_content), " chunks in total")
    for c in retrieved_content:
        llm_retrieved_chunk.append(c.page_content)

    # Search context in DB.
    search_start_time = time.time()
    similarity_results = db.similarity_search_with_score(
        query_text, k=5
    )  # [(Document(), sort_of_sim_rate)]

    # Get Chroma retrieved
    chroma_retrieved_chunk = []
    for doc, _score in similarity_results:
        chroma_retrieved_chunk.append(doc.page_content)
    print("Chroma retrieved ", len(chroma_retrieved_chunk), " in total")

    search_end_time = time.time()
    search_time = search_end_time - search_start_time
    if new_retriever:
        context_text = "\n---\n".join(llm_retrieved_chunk)
        print("context is taken out : ", search_time, "s")
    else:
        context_text = "\n\n---\n\n".join(
            [doc.page_content for doc, _score in similarity_results]
        )
        print("context is taken out : ", search_time, "s")

    # Prompt
    prompt_template = ChatPromptTemplate.from_template(prompt_template)
    prompt = prompt_template.format(context=context_text, question=query_text)
    # print('*'*25, '  prompt  ', '*'*25, flush=True)
    # print(prompt, flush=True)
    # print('*'*25, '  prompt  ', '*'*25, flush=True)
    print("prompt is created")

    # Get response from Extractor LLM
    response_start_time = time.time()
    extractor = Extractor(ext_local)
    response_text = extractor.generate_answer(prompt)
    response_end_time = time.time()
    response_time = response_end_time - response_start_time
    print("*" * 25, "  response  ", "*" * 25)
    print(response_text)
    print("*" * 25, "  response  ", "*" * 25)
    print("response is generated: ", response_time, "s")

    # Format the response
    sources = [doc.metadata.get("id", None) for doc, _score in similarity_results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    # print(formatted_response)

    append_to_csv(
        query_text,
        context_text,
        search_time,
        response_text,
        response_time,
        setup_database_time,
        similarity_results,
        logger_file_path
    )

    retrieved_info = {
            "new_prediction": new_retriever,
            "retriever_type": retriever_type,
            "question": query_text,
            "prediction": response_text,
            "llm_chunks": llm_retrieved_chunk,
            "chroma_chunks": chroma_retrieved_chunk
    }

    return retrieved_info


if __name__ == "__main__":
    main(True, True)
