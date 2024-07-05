import pandas as pd
import json
CSV_FILE_PATH="/Users/naman/Documents/groupProject/green-software-foundation/Rag/logger/parsedResults.csv"
COMBINED_RESULTS_PATH="/Users/naman/Documents/groupProject/green-software-foundation/Rag/logger/COMBINED_RESULTS.csv"

def read_ecoDoc_results(csv_file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Convert the DataFrame to a list of dictionaries
    return df.to_dict(orient="records")


def add_parsed_results(logger_file_path,combined_path):
    records=read_ecoDoc_results(logger_file_path)
    conclusion_arr=[]
    explanation_arr=[]
    result_arr=[]
    for item in records:
        generated_response=item["response_text"]
        explanation,final_answer,result=parse_generated_response(generated_response)
        explanation_arr.append(explanation)
        conclusion_arr.append(final_answer)
        result_arr.append(result)
    print("hello")
     # Add the new columns to the DataFrame
    df = pd.DataFrame(records)
    
    # Add the new columns to the DataFrame
    df['explanation'] = explanation_arr
    df['conclusion'] = conclusion_arr
    df['result'] = result_arr

    # Save the updated DataFrame to a CSV file
    df.to_csv(combined_path, index=False)

def parse_generated_response(generated_response):
     # Extract the explanation
    if "about scaling down applications during idle periods." in generated_response:
        print("hello")
    response_start = None
    if "Response:" in generated_response:
        response_start = generated_response.find("Response:") + len("Response:")
    elif "**Response**:" in generated_response:
        response_start = generated_response.find("**Response**:") + len("**Response**:")
    elif "Answer:" in generated_response:
        response_start = generated_response.find("Answer:") + len("Answer:")
    elif "**Answer**:" in generated_response:
        response_start = generated_response.find("**Answer**:") + len("**Answer**:")
    
    if response_start is not None:
        response_end = generated_response.find("Conclusion:")
        if response_end == -1:  # if "**Conclusion**:" is not found
            response_end = generated_response.find("**Conclusion**")
        if response_end == -1:  # if "Conclusion:" is not found
            response = generated_response[response_start:].strip()
        else:
            response = generated_response[response_start:response_end].strip()
    else:
        response = ""
    
    # Extract the conclusion
    conclusion_start = None
    if "Conclusion:" in generated_response:
        conclusion_start = generated_response.find("Conclusion:") + len("Conclusion:")
    elif "**Conclusion**:" in generated_response:
        conclusion_start = generated_response.find("**Conclusion**:") + len("**Conclusion**:")
    
    if conclusion_start is not None:
        conclusion = generated_response[conclusion_start:].strip()
    else:
        conclusion = ""    

    # Extract the result
    result = categorize_text(conclusion)
    
    return response, conclusion, result

def categorize_text(text):
    # Convert text to lowercase to ensure case-insensitive matching
    text_lower = text.lower()
    
    # Define keyword arrays for each category
    yes_keywords = ['yes', 'yes,']
    no_keywords = ['not applicable']
    
    # Check for keywords corresponding to each category
    if any(keyword in text_lower for keyword in yes_keywords):
        return 'Yes'
    elif any(keyword in text_lower for keyword in no_keywords):
        return 'Not Applicable'
    else:
        return 'No'



def export_combined_results_to_json(combined_results_path):
    with open("/Users/naman/Documents/groupProject/green-software-foundation/frontend/src/api_results/categories.json", "r", encoding="utf-8") as file:
        categories_json = json.load(file)["Questions"]
        
    df = pd.read_csv(combined_results_path)
    
    records=df.to_dict(orient="records")
    result_arr=[]
    for item in records:
        
        obj={}
        obj["query"] = "" if pd.isna(item["query"]) else item["query"]
        obj["explanation"] = "" if pd.isna(item["explanation"]) else item["explanation"]
        obj["result"] = "" if pd.isna(item["result"]) else item["result"]

        for question in categories_json:
            if item["query"] in question["query"]:
                obj["category"]=question["category"]
                obj["practice"]=question["practice"]
                obj["type"]=question["type"]

        if "type" in obj and obj["type"] is not None:
             result_arr.append(obj)

    with open("/Users/naman/Documents/groupProject/green-software-foundation/frontend/src/api_results/graphResponse.json", "w") as f:
            json.dump(result_arr, f)



# add_parsed_results(CSV_FILE_PATH)
# export_combined_results_to_json(COMBINED_RESULTS_PATH)