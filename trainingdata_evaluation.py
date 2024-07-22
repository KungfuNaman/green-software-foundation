import json
from langchain_community.llms.ollama import Ollama
import os
from langchain.prompts import ChatPromptTemplate

LLM_MODEL = os.getenv("LLM_MODEL")

# Get queires list
def get_all_data_to_lst(combined_dict):
  res = []
  count1 = 0
  for i,q_lst in combined_dict.items():
    for j in q_lst:
      if count1 >= 1000:
        break
      res.append(j)
      count1 += 1
  return res

def test_ollama_model(dataset_path, model):
    with open(dataset_path, 'r') as file:
        dataset = json.load(file)
    with open("Rag/prompts/prompt.json", 'r') as file:
        prompts = json.load(file)
    count = 0
    dataset = get_all_data_to_lst(dataset)

    for data in dataset:
        # if count >= 100:
        #     break
        
        question = data['query']
        context = data['context']
        expected_response = data['judgement']+", "+data['explanation']

        PROMPT_ID="P3"

        prompt_template=prompts[PROMPT_ID]
        prompt_template = ChatPromptTemplate.from_template(prompt_template)
        prompt = prompt_template.format(context=context, question=question)
        # Pass the question and context to the ollama model
        predicted_response = model.invoke(prompt)

        if "yes" in expected_response.lower():
            expected_response = "Yes"
        elif "no" in expected_response.lower() or "not applicable" in expected_response.lower():
            expected_response = "No"
        if "yes" in predicted_response.lower():
            predicted_response = "Yes"
        elif "no" in predicted_response.lower() or "not applicable" in predicted_response.lower():
            predicted_response = "No"
        
        if predicted_response == expected_response:
           count += 1
        # Compare the predicted response with the expected response
        # print("*"*50)
        # print(expected_response)
        # print("="*50)
        # print(predicted_response)
        # print("*"*50)
        # print("\n\n\n")
        # count += 1
        print(count)
    print(f"Accuracy: {count/len(dataset)}")

PROMPT = """Act as a professional assistant in the field of software development, 
you need to give precise and short answers to respond to the question that I gave.\n
I will take the corresponding text snippet from the design file of the software development, 
and you need to use a certain format and \"yes/no/not applicable\" to answer the question.\n\n
My Input would be:\n\"\"\nAnswer the question based only on the following context:\n<context>\n\nQuestion:\n<question>\n\"\"\n\n
For My Input:\n<context>: Five paragraphs excerpted from my design document for software development.\n
<question>: I'll ask you if this uses a certain technology to support a certain green practice. 
Your Answer must adhere to this format:\n\"\"\nResponse:\nJudgement: Print <Yes> / <No> / <Not Applicable> only.\n
Explanation: <The description of the reason for the judgment above>\n\"\"\n\n
For Your Answer:\n\nIn judgment,\n
<Yes> means that in the context of my question, there exists a technology or green practice that is relevant to the question.\n
<No> means that in the context of my question, there is no technology or green practice that is relevant to the question.\n
<Not Applicable> means that in the context of my question, this application is not applicable to this technique or to the green practice, e.g., applications that need to focus on real-time feedback, such as online games, are not applicable to the green practice of \"cache static data\".\n\n
In Explanation, you need to explain the judgment you made above in less than 3 sentences.\n\n
"""

# Example usage
dataset_path = 'combined_trainingset.json'
model = Ollama(model=LLM_MODEL, temperature=0.8,
                                template="""{{ if .System }}<|system|>
                                            {{ .System }}<|end|>
                                            {{ end }}{{ if .Prompt }}<|user|>
                                            {{ .Prompt }}<|end|>
                                            {{ end }}<|assistant|>
                                            {{ .Response }}<|end|>""",
                                system=PROMPT)
test_ollama_model(dataset_path, model)
