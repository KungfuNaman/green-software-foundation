import pandas as pd
import json

# Read the CSV file into a DataFrame
csv_file_path = 'Rag/logger/llmResponse1.csv'
df = pd.read_csv(csv_file_path)

# Convert the DataFrame to JSON
json_data = df.to_json(orient='records')

# If you want the JSON as a Python dictionary
json_dict = json.loads(json_data)

list=[]
count=1
for item in json_dict:
    
    query="Using the above pdf and the query : "+ item["query"] + "can you tell what is missing in the context and is the response correct? context : " + item["context_text"] + "response : " + item["response_text"]
    # obj={}
    # obj["question"]=query
    if(count>=51 and count<=67):
        list.append(query)
    count=count+1




# Output the JSON data
print(json_data)

# Optionally, save the JSON data to a file
with open('output.json', 'w') as json_file:
    json.dump(list, json_file, indent=4)