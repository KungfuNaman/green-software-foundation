from fastapi import FastAPI
from components.Generator import Generator
import json
# from some_module import some_function  # Adjust the import according to your function location
from components.FileInputHelper import FileInputHelper
from components.FileOutputHelper import FileOutputHelper
from components.Generator import Generator
from main import get_paths, initilise_embedder_retriver
from query_data import query_rag
from pydantic.dataclasses import dataclass


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}

@dataclass
class EcodocRequest:
    doc_name: str
    q_question: str

with open("Rag/prompts/prompt.json", 'r') as file:
    prompts_file = json.load(file)

@app.post("/ask_ecodoc")
def ask_ecodoc(request: EcodocRequest):
    doc_name=request.doc_name
    q_question=request.q_question

    instruction = """
       Answer this question and give the response in the jsonFormat and fill in your response in place of output  
       Json format is { result : output }
        """
    # ============================================    CONFIG    ============================================

    prompt_id = "P3"  # Choose From: P1, P2, P3, GROUND_TRUTH_PROMPT
    prompt_template = prompts_file[prompt_id]
    embedder_name, generator_name = "llama2", "llama2"
    db_collection_name = doc_name + "_" + embedder_name
    retriever_type = "chroma"   # Choose From: chroma, multiquery, ensemble

    fi_helper, fo_helper = FileInputHelper(create_doc=True), FileOutputHelper()
    document_path, logger_file_path, combined_path = get_paths(doc_name, prompt_id, generator_name)
    retriever,setup_db_time=initilise_embedder_retriver(retriever_type,embedder_name,document_path,db_collection_name,fi_helper)
    
    prompt,response_info = query_rag(retriever, prompt_template, q_question)
    generator = Generator(run_local=True,model_name="llama2",instruction=instruction)
    response_text = generator.generate_answer(prompt)

    return {"result": response_text}

# Add more endpoints as needed

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
