import dspy
from dspy.retrieve.chromadb_rm import ChromadbRM
import os
from get_embedding_function import get_embedding_function
from populate_database import setup_database

CHROMA_PATH = os.getenv("CHROMA_PATH")

query = "What is the number of tiers in the system architecture? Are there mentions of presentation, application, and database tiers?"

DOCUMENT_PATH="./documents/3.pdf"

emb_local = True

setup_database(DOCUMENT_PATH, True, emb_local, True)

embedder, collection_name = get_embedding_function(run_local=True)

retriever_model = ChromadbRM(
    collection_name,
    CHROMA_PATH,
    embedding_function=embedder.embed_query,
    k=5
)

lm = dspy.OllamaLocal(model='phi3')
# #print(lm.basic_request("What is the number of tiers in the system architecture? Are there mentions of presentation, application, and database tiers?"))
dspy.settings.configure(lm=lm, rm=retriever_model)

# # class BasicQA(dspy.Signature):
# #     """Answer questions with short factoid answers."""

# #     question = dspy.InputField()
# #     answer = dspy.OutputField(desc="often between 1 and 5 words")

# # # Define the predictor.
# # generate_answer = dspy.Predict(BasicQA)

# # # Call the predictor on a particular input.
# # pred = generate_answer(question=query)

# # # Print the input and the prediction.
# # print(f"Question: {query}")
# # print(f"Predicted Answer: {pred.answer}")

class GenerateAnswer(dspy.Signature):
    """Answer questions with short factoid answers."""

    context = dspy.InputField(desc="may contain relevant facts")
    question = dspy.InputField()
    answer = dspy.OutputField(desc="often between 30 and 50 words")



class RAG(dspy.Module):
    def __init__(self, num_passages=3):
        super().__init__()

        self.retrieve = dspy.Retrieve(k=num_passages)
        self.generate_answer = dspy.ChainOfThought(GenerateAnswer)
    
    def forward(self, question):
        context = self.retrieve(question).passages
        prediction = self.generate_answer(context=context, question=question)
        print(prediction.answer)
        return dspy.Prediction(context=context, answer=prediction.answer)
    
RAG().forward(query)
print(lm.inspect_history(n=1))


