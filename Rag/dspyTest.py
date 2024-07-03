import dspy
from dspy.retrieve.chromadb_rm import ChromadbRM
import os
from get_embedding_function import get_embedding_function
from populate_database import setup_database
from dspy.teleprompt import BootstrapFewShot
import pandas as pd
from dspy.datasets.dataset import Dataset
from dspy.evaluate.evaluate import Evaluate

TRAINING_DATA = "dataset.csv"

class CSVDataset(Dataset):
    def __init__(self, file_path, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        df = pd.read_csv(file_path)
        self._train = df.iloc[0:30].to_dict(orient='records')

        self._dev = df.iloc[30:].to_dict(orient='records')

dataset = CSVDataset(TRAINING_DATA)

trainset = [x.with_inputs('question') for x in dataset.train]
devset = [x.with_inputs('question') for x in dataset.dev]

CHROMA_PATH = os.getenv("CHROMA_PATH")

DOCUMENT_PATH="./documents/3.pdf"

emb_local = False

#setup_database(DOCUMENT_PATH, True, emb_local, True)

embedder, collection_name = get_embedding_function(run_local=emb_local)

retriever_model = ChromadbRM(
    collection_name,
    CHROMA_PATH,
    embedding_function=embedder.embed,
    k=5
)

lm = dspy.OllamaLocal(model='phi3')

dspy.settings.configure(lm=lm, rm=retriever_model)

class GenerateAnswer(dspy.Signature):
    #"""Answer questions with a short reasoning followed by a concrete conclusion. In the conclusion, answer yes when you agree with the question, no when you disagree and the question is relevant to the context, or not applicable when the question is not relevant to the context."""
    """Give a concrete yes/no/not applicable answer to a question based on a context."""

    context = dspy.InputField(desc="may contain relevant facts")
    question = dspy.InputField()
    answer = dspy.OutputField(desc="Write either Yes, No, or Not Applicable.")

class RAG(dspy.Module):
    def __init__(self, num_passages=3):
        super().__init__()

        self.retrieve = dspy.Retrieve(k=num_passages)
        self.generate_answer = dspy.ChainOfThought(GenerateAnswer)
    
    def forward(self, question):
        context = self.retrieve(question).passages
        prediction = self.generate_answer(context=context, question=question)
        return dspy.Prediction(context=context, answer=prediction.answer)

#RAG().forward(query)
#print(lm.inspect_history(n=1))
       
def validate_context_and_answer(example, pred, trace=None):
    answer_EM = dspy.evaluate.answer_exact_match(example, pred)
    answer_PM = dspy.evaluate.answer_passage_match(example, pred)
    return answer_EM and answer_PM

teleprompter = BootstrapFewShot(metric=validate_context_and_answer)

compiled_rag = teleprompter.compile(RAG(), trainset=trainset)

evaluate_on_dataset = Evaluate(devset=devset, num_threads=1, display_progress=True, display_table=5)

#Evaluate the `compiled_rag` program with the `answer_exact_match` metric.
metric = dspy.evaluate.answer_exact_match
evaluate_on_dataset(compiled_rag, metric=metric)

