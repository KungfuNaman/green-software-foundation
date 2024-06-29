import pandas as pd

CSV_FILE_PATH="/Users/naman/Documents/groupProject/green-software-foundation/Rag/logger/test.csv"
def read_ecoDoc_results(csv_file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Convert the DataFrame to a list of dictionaries
    return df.to_dict(orient="records")


def add_parsed_results(csv_file_path):
    records=read_ecoDoc_results(csv_file_path)
    final_answer_arr=[]
    explanation_arr=[]
    result_arr=[]
    for item in records:
        generated_response=item["response_text"]
        explanation,final_answer,result=parse_generated_response(generated_response)
        explanation_arr.append(explanation)
        final_answer_arr.append(final_answer)
        result_arr.append(result)
    print("hello")
    # updated_records = pd.DataFrame(records)
    # updated_records.to_csv('path/to/your/updated_records.csv', index=False)

def parse_generated_response(generated_response):
     # Extract the explanation
    response_start = generated_response.find("Response:") + len("Response:")
    response_end = generated_response.find("Conclusion:")
    response = generated_response[response_start:response_end].strip()
    
    # Extract the conclusion
    conclusion_start = generated_response.find("Conclusion:") + len("Conclusion:")
    conclusion = generated_response[conclusion_start:].strip()

    # Extract the result
    result = categorize_text(conclusion)
    
    return response, conclusion, result

def categorize_text(text):
    # Convert text to lowercase to ensure case-insensitive matching
    text_lower = text.lower()
    
    # Define keyword arrays for each category
    yes_keywords = ['yes', 'yes,']
    no_keywords = ['no', 'no,']
    
    # Check for keywords corresponding to each category
    if any(keyword in text_lower for keyword in yes_keywords):
        return 'Yes'
    elif any(keyword in text_lower for keyword in no_keywords):
        return 'No'
    else:
        return 'Not Applicable'

add_parsed_results(CSV_FILE_PATH)
