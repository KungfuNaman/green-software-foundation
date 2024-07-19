import datasets
from tqdm.auto import tqdm
import json
import os
import csv
from query_data import query_rag
from langchain_community.llms.ollama import Ollama

# TODO: Replace with custom datasets
eval_dataset = datasets.load_dataset("m-ric/huggingface_doc_qa_eval", split="train")
CSV_FILE_PATH = "Rag/logger/rag_eval.csv"


def append_to_csv(question, answer, true_answer, eval_score, eval_feedback):
    """add data to local csv and mongo cloud"""
    header = [
        "question",
        "answer",
        "true_answer",
        "eval_score",
        "eval_feedback",
    ]
    row = [
        question, 
        answer,
        true_answer,
        eval_score,
        eval_feedback,
    ]

    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(CSV_FILE_PATH), exist_ok=True)

        file_exists = os.path.isfile(CSV_FILE_PATH)

        with open(CSV_FILE_PATH, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if not file_exists:  # If file does not exist, write the header
                writer.writerow(header)
            writer.writerow(row)
    except IOError as e:
        print(f"An error occurred while writing to the CSV file: {e}")

def run_rag_tests(
    eval_dataset: datasets.Dataset,
    output_file: str,
):
    """Runs RAG tests on the given dataset and saves the results to the given output file."""
    try:  # load previous generations if they exist
        with open(output_file, "r") as f:
            outputs = json.load(f)
    except:
        outputs = []

    for example in tqdm(eval_dataset):
        question = example["question"]
        if question in [output["question"] for output in outputs]:
            continue

        answer = query_rag(question, 0, True, True)
        print("=======================================================")
        print(f"Question: {question}")
        print(f"Answer: {answer}")
        print(f'True answer: {example["answer"]}')
        result = {
            "question": question,
            "true_answer": example["answer"],
            "source_doc": example["source_doc"],
            "generated_answer": answer,
        }
        outputs.append(result)

        with open(output_file, "w") as f:
            json.dump(outputs, f)

EVALUATION_PROMPT = """###Task Description:
An instruction (might include an Input inside it), a response to evaluate, a reference answer that gets a score of 5, and a score rubric representing a evaluation criteria are given.
1. Write a detailed feedback that assess the quality of the response strictly based on the given score rubric, not evaluating in general.
2. After writing a feedback, write a score that is an integer between 1 and 5. You should refer to the score rubric.
3. The output format should look as follows: \"Feedback: {{write a feedback for criteria}} Result: {{an integer number between 1 and 5}}\"
4. Please do not generate any other opening, closing, and explanations. Be sure to include 'Result:' in your output.

###The instruction to evaluate:
{instruction}

###Response to evaluate:
{response}

###Reference Answer (Score 5):
{reference_answer}

###Score Rubrics:
[Is the response correct, accurate, and factual based on the reference answer?]
Score 1: The response is completely incorrect, inaccurate, and/or not factual.
Score 2: The response is mostly incorrect, inaccurate, and/or not factual.
Score 3: The response is somewhat correct, accurate, and/or factual.
Score 4: The response is mostly correct, accurate, and factual.
Score 5: The response is completely correct, accurate, and factual.

###Feedback:"""

from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import SystemMessage
from langchain.chat_models.base import BaseChatModel


evaluation_prompt_template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content="You are a fair evaluator language model."),
        HumanMessagePromptTemplate.from_template(EVALUATION_PROMPT),
    ]
)

# from langchain.chat_models import ChatOpenAI

# eval_chat_model = ChatOpenAI(model="gpt-4-1106-preview", temperature=0.5)
evaluator_name = "llama2"

# from langchain_community.llms import HuggingFaceHub

# repo_id = "HuggingFaceH4/zephyr-7b-beta"
# READER_MODEL_NAME = "zephyr-7b-beta"
# HUGGINGFACEHUB_API_TOKEN = "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"

# READER_LLM = HuggingFaceHub(
#     repo_id=repo_id,
#     task="text-generation",
#     model_kwargs={
#         "max_new_tokens": 512,
#         "top_k": 30,
#         "temperature": 0.1,
#         "repetition_penalty": 1.03,
#     },
#     huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,    
# )


def evaluate_answers(
    answer_path: str,
    # eval_chat_model: BaseChatModel,
    evaluator_name: str,
    evaluation_prompt_template: ChatPromptTemplate,
) -> None:
    """Evaluates generated answers. Modifies the given answer file in place for better checkpointing."""
    answers = []
    if os.path.isfile(answer_path):  # load previous generations if they exist
        answers = json.load(open(answer_path, "r"))

    for experiment in tqdm(answers):
        if f"eval_score" in experiment:
            continue

        eval_prompt = evaluation_prompt_template.format_messages(
            instruction=experiment["question"],
            response=experiment["generated_answer"],
            reference_answer=experiment["true_answer"],
        )
        eval_result = model.invoke(eval_prompt)
        feedback, score = [item.strip() for item in eval_result.split("Result:")]
        experiment[f"eval_score_{evaluator_name}"] = score
        experiment[f"eval_feedback_{evaluator_name}"] = feedback

        with open(answer_path, "w") as f:
            json.dump(answers, f)
        
        append_to_csv(experiment["question"],experiment["generated_answer"],experiment["true_answer"],score,feedback)

# Change to any other models as needed
model = Ollama(model="llama2")

for chunk_size in [200]:  # Add other chunk sizes (in tokens) as needed
    for embeddings in ["thenlper/gte-small"]:  # Add other embeddings as needed
        for rerank in [True, False]:
            #settings_name = f"chunk:{chunk_size}_embeddings:{embeddings.replace('/', '~')}_rerank:{rerank}_reader-model:{READER_MODEL_NAME}"
            output_file_name = f"./Rag/logger/rag_eval_{evaluator_name}.json"

            print("Loading knowledge base embeddings...")

            print("Running RAG...")
            run_rag_tests(
                eval_dataset=eval_dataset,
                output_file=output_file_name,
            )

            print("Running evaluation...")
            evaluate_answers(
                output_file_name,
                # eval_chat_model,
                evaluator_name,
                evaluation_prompt_template,
            )
