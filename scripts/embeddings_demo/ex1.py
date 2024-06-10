from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import pandas as pd


TRAIN_PATH = "training_data/train.csv"

load_dotenv()


# 1. finetuning -> make LLM to bahave in a certain way (text generator)
# 2. embeddings -> transfer text to vectors, vector database, 
# input -> vector db, system can return the most similar text/knowledge back

# vectors = similarity of one word in different aspects/topic/concept
# elephant = ("animal":0.8, tiger: 0.7, tree: 0.01)

# 0. Prep database
# df = pd.DataFrame(pd.read_excel("training_data/aws_pillar.xls"))
# df.to_csv(TRAIN_PATH, index=None, header=True)


# 1. Vectorize
loader = CSVLoader(file_path=TRAIN_PATH)
document = loader.load()

embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(documents=document, embedding=embeddings)


# 2. Search top similarity
def retrieve_info(query):
    # k-nearest node KNN
    similar_response = db.similarity_search(query, k=3)
    
    page_contents_array = [doc.page_content for doc in similar_response]
    
    print(page_contents_array)
    
    return page_contents_array


# 3. Setup LLM & Prompts
llm = ChatOpenAI(temperature=0, model="gpt-4")

template = """
You are a wold class software development representative that focus on the sustainability.
You'll analyze the input and figure out if each section meets best practices or not.

I will share a software design with you and you will give me the analysis and recommodation on 
every single format it covers, which based on the best practices. 
And you will follow All of the rules below:

1/ Response should be complied with the best practices regualtion.

2/ For hardware parts that are not clear in the design document, it is necessary to recommand some common hardwares in both sustainability-driven and performance_driven.

Below is a design information of the software:
{message}

Here is a best practice of sustainable software development:
{best_practice}

Please do your best to critically analyze and evaluate the strengths, weaknesses, and impacts of each environment in which the software is designed.
"""

prompt = PromptTemplate(
    input_variables=["message", "best_practice"],
    template=template
)

chain = LLMChain(llm=llm, prompt=prompt)


# 4. Final organization
def generate_response(message):
    best_practice = retrieve_info(message)
    response = chain.run(message=message, best_practice=best_practice)
    return response

# msg is from file
message = """
This document is the first approach to present the information of this project in a structured 
fashion and discuss its architecture. It also provides guidelines for the upcoming half-to-a-year 
development.
Whenever possible, we make use of existing technology instead of reinventing the wheel and 
the usability of the system is taken into account as the #1 priority.
The structure that the rest of the document will follow is:
1. A summarized description of the software architecture, including major components 
and their interactions.
2. Architectural constraints and decisions.
3. A detailed description of each component.
4. System functionality represented by use cases.
5. An outline description of the hardware and software platforms on which the system has 
been tested so far. Also, where preliminary tests and analysis show they could initially 
be deployed into.
6. A guide on how to run test cases of the application.
The physical system is formed by two main sub-networks: inside the SVT Analytics premises 
and inside any client premises.
The first one is where the developers have their workstations to work. There is a server and a 
database for development purposes and a server and a database for testing. There's also a 
bunch of cameras and a server for computing the headcount on those cameras. This server 
fills both the development and testing databases.
The workstations are connected to the internet through a router behind a firewall, for security 
concerns. Inside the company premises there's the same entry configuration.
However, the only machine that can be accessed is the web server. The database is filled by 
both the web server and the computer vision system. The cameras send a live stream to the 
computer vision system.
All the network connections are wired, except the surveillance cameras' one, which is wireless.
If it's not feasible to have separate network connections between servers that don't need to be 
connected, it's possible to join them in a single network but the server should be in a separate 
one that has access to the Internet. Inside the SVT Analytics ideally only the workstations 
should have access to the Internet.
The current status, however, is another one inside the SVT Analytics premises: the 
development server and database, and the computer vision developing system are all inside 
the single development workstation that we have right now. Our testing server and database, 
and the computer vision testing system are outside the premises, inside the InReality company 
premises.
Combining systems into a single computer is not recommended, mainly for performance 
issues.
"""
res = generate_response(message)
print(res)