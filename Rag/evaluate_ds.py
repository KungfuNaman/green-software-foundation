from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain_community.llms.ollama import Ollama
from populate_database import setup_database
from rag_utils import load_chroma_db
import json
import os
import re
import csv
import pandas as pd
from IPython.display import display
pd.set_option("display.max_colwidth", None)

DOCUMENT_PATH="documentsFromText/hadoop/content.txt"
CREATE_DOC = False
emb_local = True
CSV_FILE_PATH = "Rag/logger/QA_generated.csv"

setup_database(DOCUMENT_PATH, reset=False, emb_local=True,create_doc=CREATE_DOC)


model = Ollama(model="mistral")

def generate_answer(prompt):
    response_text = model.invoke(prompt)
    return response_text

def append_to_csv(context, question, answer):
    """add data to local csv and mongo cloud"""
    header = [
        "context_text",
        "question_text",
        "answer_text",
    ]
    row = [
        context,
        question, 
        answer,
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

QA_generation_prompt = """
Your task is to write a factoid question and an answer given a context.
Your factoid question should be related to the sence of sustainability and green software development.
Your factoid question should be answerable with a specific, concise piece of factual information from the context.
Your factoid question should be formulated in the same style as questions users could ask in a search engine.
This means that your factoid question MUST NOT mention something like "according to the passage" or "context".

Provide your answer as follows:

Output:::
Factoid question: (your factoid question)
Answer: (your answer to the factoid question)

Now here is the context.

Context: {context}\n
Output:::"""

## Generating QA couples

N_GENERATIONS = 10  # We intentionally generate only 10 QA couples here for cost and time considerations

print(f"Generating {N_GENERATIONS} QA couples...")

db = load_chroma_db(emb_local)

outputs = []
with open("./Rag/prompts/queries.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    # Step 2: Extract the 'query' field
queries = data.get("queries", [])
count = 0
contexts = []

for query_obj in queries:
    query_text = query_obj.get("query", "")
    print("query_text: ",query_text)
    count=count+1
    if count > 10:
        break
    similarity_results = db.similarity_search_with_score(query_text, k=5)  # [(Document(), sort_of_sim_rate)]
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in similarity_results])
    contexts.append(context_text)


for sampled_context in contexts:
    # Generate QA couple
    output_QA_couple = generate_answer(QA_generation_prompt.format(context=sampled_context))
    try:
        question = output_QA_couple.split("Factoid question: ")[-1].split("Answer: ")[0]
        answer = output_QA_couple.split("Answer: ")[-1]
        assert len(answer) < 300, "Answer is too long"
        append_to_csv(sampled_context, question, answer)

        outputs.append(
            {
                "context": sampled_context,
                "question": question,
                "answer": answer,
            }
        )
    except:
        continue



# Setup critique agents
# TODO: Add more/modify critique prompts as needed

question_groundedness_critique_prompt = """
You will be given a context and a question.
Your task is to provide a 'total rating' scoring how well one can answer the given question unambiguously with the given context.
Give your answer on a scale of 1 to 5, where 1 means that the question is not answerable at all given the context, and 5 means that the question is clearly and unambiguously answerable with the context.

Provide your answer as follows:

Answer:::
Evaluation: (your rationale for the rating, as a text)
Total rating: (your rating, as a number between 1 and 5)

You MUST provide values for 'Evaluation:' and 'Total rating:' in your answer.

Now here are the question and context.

Question: {question}\n
Context: {context}\n
Answer::: """

question_relevance_critique_prompt = """
You will be given a question.
Your task is to provide a 'total rating' representing how useful this question can be to software developers for improving the sustainability of their project.
Give your answer on a scale of 1 to 5, where 1 means that the question is not useful at all, and 5 means that the question is extremely useful.

Provide your answer as follows:

Answer:::
Evaluation: (your rationale for the rating, as a text)
Total rating: (your rating, as a number between 1 and 5)

You MUST provide values for 'Evaluation:' and 'Total rating:' in your answer.

Now here is the question.

Question: {question}\n
Answer::: """

question_standalone_critique_prompt = """
You will be given a question.
Your task is to provide a 'total rating' representing how context-independant this question is.
Give your answer on a scale of 1 to 5, where 1 means that the question depends on additional information to be understood, and 5 means that the question makes sense by itself.
For instance, if the question refers to a particular setting, like 'in the context' or 'in the document', the rating must be 1.
The questions can contain obscure technical nouns or acronyms like Gradio, Hub, Hugging Face or Space and still be a 5: it must simply be clear to an operator with access to documentation what the question is about.

For instance, "What is the name of the checkpoint from which the ViT model is imported?" should receive a 1, since there is an implicit mention of a context, thus the question is not independant from the context.

Provide your answer as follows:

Answer:::
Evaluation: (your rationale for the rating, as a text)
Total rating: (your rating, as a number between 1 and 5)

You MUST provide values for 'Evaluation:' and 'Total rating:' in your answer.

Now here is the question.

Question: {question}\n
Answer::: """


print("Generating critique for each QA couple...")
for output in outputs:
    evaluations = {
        "groundedness": generate_answer(
            question_groundedness_critique_prompt.format(
                context=output["context"], question=output["question"]
            ),
        ),
        "relevance": generate_answer(
            question_relevance_critique_prompt.format(question=output["question"]),
        ),
        "standalone": generate_answer(
            question_standalone_critique_prompt.format(question=output["question"]),
        ),
    }
    try:
        for criterion, evaluation in evaluations.items():
            # scores = evaluation.split("Total rating: ")[-1].strip()
            # if not scores.isdigit():
            #     scores = scores.split("\n")[0]
            score, eval = (
                float(re.findall(r"\d+\.?\d*",evaluation.split("Total rating: ")[-1].strip())[0]),
                evaluation.split("Total rating: ")[-2].split("Evaluation: ")[1],
            )
            output.update(
                {
                    f"{criterion}_score": score,
                    f"{criterion}_eval": eval,
                }
            )
    except Exception as e:
        print(f"An error occurred while processing the critique: {e}")
        continue


#Save the outputs to a CSV file
df = pd.DataFrame(outputs)
df.to_csv("Rag/logger/Evaluation.csv", index=False)

pd.set_option("display.max_colwidth", None)

generated_questions = pd.DataFrame.from_dict(outputs)

print("Evaluation dataset before filtering:")
display(
    generated_questions[
        [
            "question",
            "answer",
            "groundedness_score",
            "relevance_score",
            "standalone_score",
        ]
    ]
)
generated_questions = generated_questions.loc[
    (generated_questions["groundedness_score"] >= 4)
    & (generated_questions["relevance_score"] >= 4)
    & (generated_questions["standalone_score"] >= 4)
]
print("============================================")
print("Final evaluation dataset:")
display(
    generated_questions[
        [
            "question",
            "answer",
            "groundedness_score",
            "relevance_score",
            "standalone_score",
        ]
    ]
)

