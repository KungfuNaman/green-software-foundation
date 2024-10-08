import time
import json
from langchain.prompts import ChatPromptTemplate

from components.Embedder import Embedder
from components.Retriever import Retriever
from components.FileOutputHelper import FileOutputHelper
from components.Generator import Generator
from populate_database import setup_database


def query_rag(retriever, prompt_template_text, query_text: str):

    # Context
    search_start_time = time.time()
    retrieved_items = get_retrieved_chunks(retriever, query_text)
    context_text = get_context(retrieved_items)
    search_end_time = time.time()
    search_time = search_end_time - search_start_time
    print("context is taken out : ", search_time, "s")

    # Prompt
    prompt_template = ChatPromptTemplate.from_template(prompt_template_text)
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

    return prompt, response_info


def generate_result(generator, prompt, response_info):
    # Get response from Extractor LLM
    response_start_time = time.time()
    response_text = generator.generate_answer(prompt)
    response_end_time = time.time()
    response_time = response_end_time - response_start_time
    print("*" * 25, "  response  ", "*" * 25)
    print(response_text)
    print("*" * 25, "  response  ", "*" * 25)
    print("response is generated: ", response_time, "s")

    response_info["response_text"] = response_text
    response_info["response_time"] = response_time

    return response_text, response_info


def compare_retrieved_items(retriever_lst, prompt_template_text, query_text: str):
    retrieved_items_dict = {"question": query_text, "retrieved_chunks": {}, "prediction": {}}
    for rtype, retriever in retriever_lst:
        retrieved_items = get_retrieved_chunks(retriever, query_text)

        # retrieved content
        retrieved_content = [i.page_content for i in retrieved_items]
        print("{} retrieved {} chunks".format(rtype, len(retrieved_content)))
        retrieved_items_dict["retrieved_chunks"][rtype] = retrieved_content

        # prompt
        context_text = "\n\n---\n\n".join([doc for doc in retrieved_content])
        prompt_template = ChatPromptTemplate.from_template(prompt_template_text)
        prompt = prompt_template.format(context=context_text, question=query_text)

        # get response
        generator = Generator(run_local=False, sota_model=True)
        response_text = generator.gpt_chat(prompt=prompt)

        retrieved_items_dict["prediction"][rtype] = response_text
    return retrieved_items_dict


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

    # doc_path = "doc_data/documentsFromText/" + "Netflix" + "/content.txt"
    # coll = "test_collection"
    # _, vecdb, doc_chunks = setup_database(embedder=embedder, document_path=doc_path, collection_name=coll)

    # retriever_obj = Retriever(retriever_type="chroma", vectordb=vecdb)
    # retriever1 = retriever_obj.get_retriever()
    # generator1 = Generator(run_local=True, model_name="phi3")

    # with open("Rag/prompts/prompt_templates.json", 'r') as file:
    #     prompts_file = json.load(file)
    # pt = prompts_file["P2"]
    # qt = "Is there any mention of implementing a stateless design?"

    # prompt,response_info1 = query_rag(retriever1, pt, qt)
    # response_info1["query"] = qt
    # response_info1["setup_db_time"] = "0"
    # response_info1["logger_file_path"] = None

    # fo_helper = FileOutputHelper()
    # fo_helper.append_to_csv(response_info1)


