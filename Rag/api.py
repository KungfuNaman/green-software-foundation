from fastapi import FastAPI, HTTPException, UploadFile, Depends
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import json
import aiofiles
import re
from pathlib import Path
from pydantic.dataclasses import dataclass

from components.FileInputHelper import FileInputHelper
from components.FileOutputHelper import FileOutputHelper
from components.Generator import Generator
from main import get_paths, init_embedder, prep_db_and_chunking, init_retriever, parse_doc_path, generate_result
from query_data import query_rag
from parser import export_combined_results_to_json, add_parsed_results, export_combined_results_to_json_file
from evaluation.summary_charts import generate_pie_chart, generate_bar_chart


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

with open(CURRENT_DIR + "/prompts/prompt_templates.json", 'r') as file:
    prompts_file = json.load(file)


@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}


@app.post("/ask_ecodoc")
async def ask_ecodoc(file: UploadFile):

    cleaned_filename = re.sub(r'[^\w\-.]', '_', file.filename)
    document_path = CURRENT_DIR + "/doc_data/uploaded_docs/" + cleaned_filename
    destination = Path(document_path)

    try:
        async with aiofiles.open(destination, "wb") as buffer:
            content = await file.read() 
            await buffer.write(content)  
    except Exception as e:
        return {"message": f"An error occurred: {str(e)}"}
    
    doc_name, extension = parse_doc_path(document_path)

    # ============================================    CONFIG    ============================================

    image_extract = False
    prompt_id = "P3"  # Choose From: P1, P2, P3, P4, GROUND_TRUTH_PROMPT

    prompt_template_text = prompts_file[prompt_id]
    embedder_name, generator_name = "llama2", "phi3"
    db_collection_name = doc_name + "_" + embedder_name
    retriever_type = "chroma"  # Choose From: chroma, multiquery, ensemble, bm25, faiss
    retriever_type_lst = []  # For comparing the retrievers
    alternate_query_file_path = CURRENT_DIR + "/prompts/queries_final.json"

    fi_helper, fo_helper = FileInputHelper(create_doc=True if extension == "txt" else False), FileOutputHelper()
    logger_file_path, combined_path = (CURRENT_DIR + p for p in get_paths(doc_name, prompt_id, generator_name))

    # ============================================    PIPELINE    ================================================
    
    # Initialize Embedder
    embedder = init_embedder(embedder_name=embedder_name)

    # Prepare Database and Chunking
    setup_db_time, db, doc_chunks = prep_db_and_chunking(embedder, document_path, db_collection_name, fi_helper, image_extract)

    # Initialize Retriever 
    retriever, retriever_lst = init_retriever(retriever_type, retriever_type_lst, db, doc_chunks, embedder)

    # Initialize Generator
    generator = Generator(run_local=True, model_name=generator_name)

    # Load Query File
    try:
        query_file_path = CURRENT_DIR + "/doc_data/documentsFromText/" + doc_name + "/ground_truth.json"
        ground_truth = fi_helper.load_json_file(query_file_path)
    except FileNotFoundError:
        print("Using general queries file as do not have a ground truth for this doc.")
        query_file_path = alternate_query_file_path
        ground_truth = fi_helper.load_json_file(query_file_path)["queries"]

    truth_length = len(ground_truth)

     # Iterative Querying
    def generate_results():
        try: 
            for q_idx in range(truth_length):
                q_question = ground_truth[q_idx].get("query", "")
                # ----------     Regular Invoke & Record to CSV     ----------
                prompt, response_info = query_rag(retriever, prompt_template_text, q_question)
                response_text, response_info = generate_result(generator, prompt, response_info)
                response_info["query"] = q_question
                response_info["setup_db_time"] = setup_db_time
                response_info["logger_file_path"] = logger_file_path
                fo_helper.append_to_csv(response_info) 
                add_parsed_results(logger_file_path, combined_path, prompt_id)
                json_response = export_combined_results_to_json(combined_path) 
                yield json.dumps(json_response) + "\n"
        finally:
            # saving results to json file
            result_path = export_combined_results_to_json_file(combined_path)
            # generating charts
            generate_pie_chart(result_path)
            generate_bar_chart(result_path)
            #cleanup files
            if os.path.exists(logger_file_path):
                os.remove(logger_file_path)
            if os.path.exists(combined_path):
                os.remove(combined_path)
            if os.path.exists(document_path):
                os.remove(document_path)
            if os.path.exists(result_path):
                os.remove(result_path)
            db.delete_collection()

    return StreamingResponse(generate_results(), media_type="application/json")

@app.get("/get_sample_results/{doc_name}")
def get_sample_results(doc_name: str):
    sample_results_path = CURRENT_DIR + "/doc_data/sample_file_data/modified_results.json"
    try:
        with open(sample_results_path, 'r') as file:
            sample_results = json.load(file)
        return {"response": sample_results[doc_name]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
