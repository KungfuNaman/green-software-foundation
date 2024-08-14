import pandas as pd
import json


def read_ecoDoc_results(csv_file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Convert the DataFrame to a list of dictionaries
    return df.to_dict(orient="records")


def add_parsed_results(logger_file_path, combined_path, PROMPT_ID):
    records = read_ecoDoc_results(logger_file_path)
    conclusion_arr = []
    explanation_arr = []
    result_arr = []
    suggestion_arr = []
    for item in records:

        generated_response = item["response_text"]
        if isinstance(generated_response, str):
            explanation, final_answer, result, suggestion = parse_generated_response(generated_response, PROMPT_ID)
            explanation_arr.append(explanation)
            conclusion_arr.append(final_answer)
            result_arr.append(result)
            suggestion_arr.append(suggestion)
        else:
            explanation_arr.append("")
            conclusion_arr.append("")
            result_arr.append("")
            suggestion_arr.append("")
    # Add the new columns to the DataFrame
    df = pd.DataFrame(records)

    # Add the new columns to the DataFrame
    df['explanation'] = explanation_arr
    df['conclusion'] = conclusion_arr
    df['result'] = result_arr
    df['suggestion'] = suggestion_arr

    # Save the updated DataFrame to a CSV file
    df.to_csv(combined_path, index=False)


def parse_generated_response(generated_response, PROMPT_ID):
    if PROMPT_ID == "P1":
        # Extract the explanation
        if "about scaling down applications during idle periods." in generated_response:
            print("hello")
        response_start = None

        if "Response:" in generated_response:
            response_start = generated_response.find("Response:") + len("Response:")
        elif "*Response*:" in generated_response:
            response_start = generated_response.find("*Response:") + len("Response*:")
        elif "Answer:" in generated_response:
            response_start = generated_response.find("Answer:") + len("Answer:")
        elif "*Answer*:" in generated_response:
            response_start = generated_response.find("*Answer:") + len("Answer*:")

        if response_start is not None:
            response_end = generated_response.find("Conclusion:")
            if response_end == -1:  # if "*Conclusion*:" is not found
                response_end = generated_response.find("*Conclusion*")
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
        elif "*Conclusion*:" in generated_response:
            conclusion_start = generated_response.find("*Conclusion:") + len("Conclusion*:")

        if conclusion_start is not None:
            conclusion = generated_response[conclusion_start:].strip()
        else:
            conclusion = ""

        # Extract the result
        result = categorize_text(conclusion)

        return response, conclusion, result
    
    elif PROMPT_ID == "P2":
        if "Judgement:" in generated_response:
            start_keyword = "Judgement:"
        else:
            start_keyword = "Response:"
        end_keyword = "Explanation:"

        start_index = generated_response.find(start_keyword) + len(start_keyword)
        end_index = generated_response.find(end_keyword)

        # Extract and strip any leading/trailing whitespace
        judgement = generated_response[start_index:end_index].strip()
        judgement = categorize_text(judgement)
        start_keyword = "Explanation:"
        end_keyword = "Explanation:"

        start_index = generated_response.find(start_keyword) + len(start_keyword)
        end_index = generated_response.find(end_keyword)

        explanation = generated_response[start_index:].strip()

        judgement = judgement.replace(":", "").strip()
        return explanation, judgement, judgement

    elif PROMPT_ID == "P3":
        if "Judgement" in generated_response:
            start_index = generated_response.find("Judgement") + len("Judgement:")
        elif "Judgment" in generated_response:
            start_index = generated_response.find("Judgment") + len("Judgment:")
        elif "judgment" in generated_response.lower():
            start_index = generated_response.find("judgment") + len("judgment:")
        elif "Response" in generated_response:
            start_index = generated_response.find("Response") + len("Response:")
        elif "Answer" in generated_response:
            start_index = generated_response.find("Answer") + len("Answer:")
        else:
            start_index = 0

        if "Explan" in generated_response or "Explan_ment:" in generated_response or "Explan_ation:" in generated_response:
            end_index = generated_response.find("Explan") + len("Explanation:")
        elif "explan" in generated_response.lower():
            end_index = generated_response.find("explan") + len("explanation:")
        else:
            end_index = len(" Judgement - Yes")
        
        if "Suggestion" in generated_response:
            end_index2 = generated_response.find("Suggestion")+len("Suggestion:")
        else:
            end_index2 = len(generated_response)

        # Extract and strip any leading/trailing whitespace
        judgement = generated_response[start_index:end_index].strip()
        judgement = categorize_text(judgement)

        if end_index2 is not None:
            explanation = generated_response[end_index:(end_index2-len("Suggestion:"))].strip()
            suggestion = generated_response[end_index2:].strip()
        else:
            explanation = generated_response[end_index:].strip()
            suggestion = ""

        judgement = judgement.replace(":", "").strip()
        return explanation, judgement, judgement, suggestion

    return "", "", "", ""

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


def export_combined_results_to_json_file(combined_results_path):
    with open("prompts/queries_final.json", "r", encoding="utf-8") as file:
        queries = json.load(file)["queries"]

    df = pd.read_csv(combined_results_path)

    records = df.to_dict(orient="records")
    result_arr = []
    for item in records:
        obj = {}
        obj["query"] = "" if pd.isna(item["query"]) else item["query"]
        obj["explanation"] = "" if pd.isna(item["explanation"]) else item["explanation"]
        obj["result"] = "" if pd.isna(item["result"]) else item["result"]
        obj["suggestion"] = "" if pd.isna(item["suggestion"]) else item["suggestion"]

        for question in queries:
            if item["query"] in question["query"]:
                obj["category"] = question["category"]
                obj["practice"] = question["practice"]
                obj["type"] = question["type"]

        if "type" in obj and obj["type"] is not None:
            result_arr.append(obj)

    json_file = {"response": result_arr}
    graphResponsePath = combined_results_path.split("/")[-1].replace(".csv", "") + ".json"
    with open("logger/result_" + graphResponsePath, "w") as f:
        json.dump(json_file, f)
    return "logger/result_" + graphResponsePath


def export_combined_results_to_json(combined_results_path):
    with open("prompts/queries_old.json", "r", encoding="utf-8") as file:
        queries = json.load(file)["queries"]

    df = pd.read_csv(combined_results_path)

    records = df.to_dict(orient="records")
    result_arr = []
    for item in records:
        obj = {}
        obj["query"] = "" if pd.isna(item["query"]) else item["query"]
        obj["explanation"] = "" if pd.isna(item["explanation"]) else item["explanation"]
        obj["result"] = "" if pd.isna(item["result"]) else item["result"]
        obj["suggestion"] = "" if pd.isna(item["suggestion"]) else item["suggestion"]

        for question in queries:
            if item["query"] in question["query"]:
                obj["category"] = question["category"]
                obj["practice"] = question["practice"]
                obj["type"] = question["type"]

        if "type" in obj and obj["type"] is not None:
            result_arr.append(obj)

    json_response = {"response": result_arr}
    return json_response


def addCategories():
    with open("frontend/src/api_results/categories.json", "r", encoding="utf-8") as file:
        categories_json = json.load(file)["Questions"]
    with open("prompts/queries.json", "r", encoding="utf-8") as file:
        queries = json.load(file)["queries"]
    final_result = {}
    for item in categories_json:
        obj = {}
        obj["category"] = item["category"]
        obj["type"] = item["type"]
        final_result[item["practice"]] = obj

    for item in queries:
        if item["practice"] in final_result:
            item["category"] = final_result[item["practice"]]["category"]

    result_arr = {"queries": queries}

    with open("prompts/queries.json", "w") as f:
        json.dump(result_arr, f)
    print("hello")

#add_parsed_results("logger/phi3_P3_Netflix_copy_suggestions.csv","logger/phi3_P3_Netflix_suggestions_combined.csv","P3")

# files=["Netflix","Uber","Instagram","Whatsapp","Dropbox"]
# for item in files:
#     path="logger/Results_R-M_G/phi3_P2_"+item+"_combined.csv"
#     add_parsed_results("logger/Results_R-M_G/phi3_P2_"+item+".csv","logger/Results_R-M_G/phi3_P2_"+item+"_combined.csv","P2")
