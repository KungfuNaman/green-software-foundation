import json
import pandas as pd
import os
GROUND_TRUTH_PATH="documentsFromText/Whatsapp/ground_truth.json"
COMBINED_RESULT_PATH="Rag/logger/phi3_P2_Whatsapp_combined.csv"
EVAL_PATH="frontend/src/api_results/evaluation/results.json"
def combine_groundTruth_result(ground_truth_path,combined_result_path):

    with open(ground_truth_path, "r", encoding="utf-8") as file:
        ground_truth_json = json.load(file)
        ground_truth_query_map = {item['query']: {k: v for k, v in item.items() if k != 'query'} for item in ground_truth_json}

    
    df = pd.read_csv(combined_result_path)
    combined_result_records=df.to_dict(orient="records")
    combined_result_query_map = {item['query']: {k: v for k, v in item.items() if k != 'query'} for item in combined_result_records}
    
    result_arr=[]
    for key in combined_result_query_map:
        obj={}
        ground_truth_item = ground_truth_query_map.get(key) if key in ground_truth_query_map and ground_truth_query_map[key] is not None else None
        if(ground_truth_item is not None):
            llm_response_item=combined_result_query_map[key]
            obj["query"]=key
            obj["humanJudgement"]=ground_truth_item["Response"]["Judgement"]
            obj["llmJudgement"]=llm_response_item["result"]
            obj["humanExplanation"]=ground_truth_item["Response"]["Explanation"]
            obj["llmExplanation"]=llm_response_item["explanation"]
            obj["category"]=ground_truth_item["category"]
            obj["practice"]=ground_truth_item["practice"]
            obj["ecoDocContext"]=llm_response_item["context_text"]


            result_arr.append(obj)
    df = pd.DataFrame(result_arr)
    df.to_csv("./results.csv", index=False)

    return result_arr

def update_json_file(file_path, key, value):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    # Check if the file exists
    if os.path.exists(file_path):
        # Read the existing data from the file
        with open(file_path, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {}
    else:
        # Initialize an empty dictionary if the file does not exist
        data = {}

    # Update the dictionary with the new key-value pair
    data[key] = value

    # Write the updated data back to the file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def generate_eval_for_frontend(ground_truth_path,combined_result_path,eval_path):
    result_arr=combine_groundTruth_result(ground_truth_path,combined_result_path)
    # ft_phi3_P3_"+doc+"_combined.csv

    key=combined_result_path.split("/")[-2].replace("_combined.csv","").replace("ft_phi3_P3_","")+"_"+combined_result_path.split("/")[-1].replace("ft_phi3_P3_","").replace("_combined.csv","")
    update_json_file(eval_path,key,result_arr)




def modify_to_old_queries(ground_truth_path):
    old_queries_json_path="Rag/prompts/queries_old.json"
    with open(old_queries_json_path, "r", encoding="utf-8") as file:
            old_queries_arr = json.load(file)["queries"]
    with open(ground_truth_path, "r", encoding="utf-8") as file:
            ground_truth_arr = json.load(file)
    for item in old_queries_arr:
        for ground_item in ground_truth_arr:
            if ground_item["category"] == item["category"] and ground_item["practice"] == item["practice"]:
                ground_item["query"] =item["query"]

    with open(ground_truth_path, 'w') as file:
            json.dump(ground_truth_arr, file, indent=4)


# documents=["Netflix","Whatsapp","Dropbox","Instagram","Uber"]
# for doc in documents:
#     ground_truth_path="documentsFromText/"+doc+"/ground_truth.json"
#     combined_result_path="Rag/logger/Results_R-E_G/phi3_P3_"+doc+"_combined.csv"
#     eval_path="frontend/src/api_results/evaluation/results.json"
#     # modify_to_old_queries(ground_truth_path)
#     generate_eval_for_frontend(ground_truth_path,combined_result_path,eval_path)
