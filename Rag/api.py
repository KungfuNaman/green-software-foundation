from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from components.Generator import Generator
import json
from fastapi.middleware.cors import CORSMiddleware
import aiofiles
from pathlib import Path
import asyncio

# from some_module import some_function  # Adjust the import according to your function location
from components.FileInputHelper import FileInputHelper
from components.FileOutputHelper import FileOutputHelper
from components.Generator import Generator
from main import get_paths, init_embedder, prep_db_and_chunking, init_retriever, parse_doc_path, generate_result
from query_data import query_rag
from parser import export_combined_results_to_json, add_parsed_results
from pydantic.dataclasses import dataclass


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open("Rag/prompts/prompt.json", 'r') as file:
    prompts_file = json.load(file)

# @app.post("/ask_ecodoc")
# def ask_ecodoc(request: EcodocRequest):
#     doc_path=request.doc_path
#     q_question=request.q_question

#     instruction = """
#        Answer this question and give the response in the jsonFormat and fill in your response in place of output  
#        Json format is { result : output }
#         """
    
#     doc_name, extension = parse_doc_path(doc_path)
#     # ============================================    CONFIG    ============================================

#     prompt_id = "P3"  # Choose From: P1, P2, P3, GROUND_TRUTH_PROMPT
#     prompt_template = prompts_file[prompt_id]
#     embedder_name, generator_name = "llama2", "phi3"
#     db_collection_name = doc_name + "_" + embedder_name
#     retriever_type = "chroma"   # Choose From: chroma, multiquery, ensemble
#     retriever_type_lst = ["chroma", "multiquery"]  # For comparing the retrievers
#     image_extract = False

#     fi_helper, fo_helper = FileInputHelper(create_doc=True if extension == "txt" else False), FileOutputHelper()
#     logger_file_path, combined_path = get_paths(doc_name, prompt_id, generator_name)

#     # ============================================    PIPELINE    ================================================

#     # Initialize Embedder
#     embedder = init_embedder(embedder_name=embedder_name)

#     # Prepare Database and Chunking
#     setup_db_time, db, doc_chunks = prep_db_and_chunking(embedder, doc_path, db_collection_name, fi_helper, image_extract)

#     # Initialize Retriever 
#     retriever, retriever_lst = init_retriever(retriever_type,retriever_type_lst,db,doc_chunks,embedder)

#     # Initialize Generator
#     generator = Generator(run_local=True, model_name=generator_name, instruction=instruction)

#     prompt,response_info = query_rag(retriever, prompt_template, q_question)
#     response_text = generator.generate_answer(prompt)

#     return {"result": response_text}

# Add more endpoints as needed

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}

@app.post("/ask_ecodoc")
async def ask_ecodoc(file: UploadFile):
    document_path = "Rag/uploaded_docs/" + file.filename 
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
    retriever_type = "multiquery"  # Choose From: chroma, multiquery, ensemble, bm25, faiss
    retriever_type_lst = ["chroma", "multiquery", "ensemble"]  # For comparing the retrievers
    alternate_query_file_path = "./Rag/prompts/old_queries.json"  # Query file to use when ground truth is not available

    fi_helper, fo_helper = FileInputHelper(create_doc=True if extension == "txt" else False), FileOutputHelper()
    logger_file_path, combined_path = get_paths(doc_name, prompt_id, generator_name)

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
        query_file_path = "./documentsFromText/" + doc_name + "/ground_truth.json"
        ground_truth = fi_helper.load_json_file(query_file_path)
    except FileNotFoundError:
        print("Using general queries file as do not have a ground truth for this doc.")
        query_file_path = alternate_query_file_path
        ground_truth = fi_helper.load_json_file(query_file_path)["queries"]

    truth_length = len(ground_truth)

     # Iterative Querying
    async def generate_results(): 
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
            print(json.dumps(json_response) + "\n") 
            yield json.dumps(json_response) + "\n"
    
    return StreamingResponse(generate_results(), media_type="application/json")

@app.post("/ask_ecodoctest")
async def ask_ecodoctest(file: UploadFile):
    # Your existing logic
    async def generate():
        yield json.dumps({"response": [{"query": "Is there any mention of minimizing the total number of deployed environments?", "explanation": "The context provided does not discuss minimizing the total number of deployed environments, as it focuses on Git's features and benefits within software development processes.", "result": "Not Applicable", "category": "Resource Optimization", "practice": "Minimize the total number of deployed environments", "type": "web"}]}) + "\n"
        await asyncio.sleep(10)
        yield json.dumps({"response": [{"query": "Is there any mention of minimizing the total number of deployed environments?", "explanation": "The context provided does not discuss minimizing the total number of deployed environments, as it focuses on Git's features and benefits within software development processes.", "result": "Not Applicable", "category": "Resource Optimization", "practice": "Minimize the total number of deployed environments", "type": "web"} ,
        {
            "query": "Is there any mention of optimizing storage utilization?",
            "category": "Resource Optimization",
            "practice": "Optimize storage utilization",
            "result": "Yes",
            "explanation": "The context mentions the use of Amazon's large EC2 instances with InnoDB, which is known for its efficient space and performance characteristics. This choice indicates an optimization strategy to reduce latency by reducing network calls between services while improving storage utilization efficiency.",
            "type": "web"
        }]}) + "\n"
    
    return StreamingResponse(generate(), media_type="application/json")
    


@app.get("/get_sample_results/{doc_name}")
def get_sample_results(doc_name: str):
    sample_results_path = "Rag/results/modified_results.json"
    try:
        with open(sample_results_path, 'r') as file:
            sample_results = json.load(file)
        return {"response": sample_results[doc_name]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
