from fastapi import FastAPI
from components.Generator import Generator
import json
# from some_module import some_function  # Adjust the import according to your function location
from components.FileInputHelper import FileInputHelper
from components.FileOutputHelper import FileOutputHelper
from components.Generator import Generator
from main import get_paths, init_embedder, prep_db_and_chunking, init_retriever, parse_doc_path
from query_data import query_rag
from pydantic.dataclasses import dataclass


app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}


@dataclass
class EcodocRequest:
    doc_path: str
    q_question: str

with open("Rag/prompts/prompt.json", 'r') as file:
    prompts_file = json.load(file)


@app.post("/ask_ecodoc")
def ask_ecodoc(request: EcodocRequest):
    doc_path=request.doc_path
    q_question=request.q_question

    instruction = """
       Answer this question and give the response in the jsonFormat and fill in your response in place of output  
       Json format is { result : output }
        """
    
    doc_name, extension = parse_doc_path(doc_path)
    # ============================================    CONFIG    ============================================

    prompt_id = "P3"  # Choose From: P1, P2, P3, GROUND_TRUTH_PROMPT
    prompt_template = prompts_file[prompt_id]
    embedder_name, generator_name = "llama2", "phi3"
    db_collection_name = doc_name + "_" + embedder_name
    retriever_type = "chroma"   # Choose From: chroma, multiquery, ensemble
    retriever_type_lst = ["chroma", "multiquery"]  # For comparing the retrievers
    image_extract = False

    fi_helper, fo_helper = FileInputHelper(create_doc=True if extension == "txt" else False), FileOutputHelper()
    logger_file_path, combined_path = get_paths(doc_name, prompt_id, generator_name)

    # ============================================    PIPELINE    ================================================

    # Initialize Embedder
    embedder = init_embedder(embedder_name=embedder_name)

    # Prepare Database and Chunking
    setup_db_time, db, doc_chunks = prep_db_and_chunking(embedder, doc_path, db_collection_name, fi_helper, image_extract)

    # Initialize Retriever 
    retriever, retriever_lst = init_retriever(retriever_type,retriever_type_lst,db,doc_chunks,embedder)

    # Initialize Generator
    generator = Generator(run_local=True, model_name=generator_name, instruction=instruction)

    prompt,response_info = query_rag(retriever, prompt_template, q_question)
    response_text = generator.generate_answer(prompt)

    return {"result": response_text}

# Add more endpoints as needed

@app.get("/get_sample_results/{doc_name}")
def get_sample_results(doc_name: str):
    sample_results_path = "Rag/results/modified_results.json"
    with open(sample_results_path, 'r') as file:
        sample_results = json.load(file)

    try:    
        result = sample_results[doc_name]
    except KeyError:
        return {"response": "No results found for the given document name."}
    return {"response": result}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
