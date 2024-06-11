# %%
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# MODEL = "gpt-3.5-turbo"
# MODEL = "mixtral:8x7b"
MODEL = "llama2"

# %%
from langchain_community.llms import Ollama
from langchain_openai.chat_models import ChatOpenAI
from langchain_community.embeddings import OllamaEmbeddings
from langchain_openai.embeddings import OpenAIEmbeddings

if MODEL.startswith("gpt"):
    model = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model=MODEL)
    embeddings = OpenAIEmbeddings()
else:
    model = Ollama(model=MODEL)
    embeddings = OllamaEmbeddings(model=MODEL)

# %%
# Rule-based evaluation function
def evaluate_document_rule_based(document_content):
    scores = {
        "Energy Efficiency": 0,
        "Maintainability": 0,
        "Scalability": 0,
        "Green Software Compliance": 0
    }

    keywords = {
        "Energy Efficiency": ["energy-efficient", "low power", "optimized"],
        "Maintainability": ["maintainable", "easy to update", "modular"],
        "Scalability": ["scalable", "scalability", "expandable"],
        "Green Software Compliance": ["green software", "eco-friendly", "compliant"]
    }

    for criterion, words in keywords.items():
        for word in words:
            if word in document_content.lower():
                scores[criterion] += 1

    for criterion in scores:
        if scores[criterion] > 0:
            scores[criterion] = min(5, scores[criterion])
        else:
            scores[criterion] = 1

    return scores

# %%
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import DocArrayInMemorySearch
from operator import itemgetter





# Define prompt template
template = """
Extract the following information from the software architecture document and provide the details in the specified JSON structure:

structured_data = {{
    "Document Metadata": {{
        "Document ID": "",
        "Document Title": "",
        "Version": "",
        "Date": "",
        "Author": "",
        "Company": ""
    }},
    "Infrastructure Details": {{
        "Servers": [
            {{
                "Type": "",
                "Quantity": 0,
                "Power Consumption": 0.0
            }},
            {{
                "Type": "",
                "Quantity": 0,
                "Power Consumption": 0.0
            }},
            {{
                "Type": "",
                "Quantity": 0,
                "Power Consumption": 0.0
            }}
        ],
        "Data Centers": {{
            "Location": "",
            "Energy Source": ""
        }}
    }},
    "Software Architecture": {{
        "Deployment Model": {{
            "Architecture": "",
            "Clustering": ""
        }},
        "Software Layers": {{
            "Presentation Layer": "",
            "Control Layer": "",
            "Resource Layer": "",
            "Domain Layer": "",
            "Common Elements Layer": ""
        }}
    }},
    "Operational Details": {{
        "Transactions": {{
            "Average Daily Transactions": 0,
            "Peak Usage Times": ""
        }},
        "User Base": {{
            "Number of Individual Users": 0,
            "Number of Corporate Users": 0
        }}
    }},
    "Security and Compliance": {{
        "Security Measures": {{
            "Authentication": "",
            "Authorization": "",
            "Encryption": ""
        }},
        "Compliance Requirements": ""
    }},
    "Performance and Reliability": {{
        "Performance Metrics": {{
            "Response Time": "",
            "Scalability": ""
        }},
        "Availability": {{
            "Uptime Requirements": "",
            "Failover Mechanisms": ""
        }}
    }},
    "Internationalization": {{
        "Supported Languages": [],
        "Localization Features": ""
    }},
    "Data Persistence": {{
        "Database Type": "",
        "Storage Requirements": "",
        "Backup and Recovery": ""
    }},
    "Quality Attributes": {{
        "Scalability": "",
        "Reliability": "",
        "Portability": "",
        "Security": ""
    }}
}}

Context: {context}

"""

prompt = PromptTemplate.from_template(template)

# Load and split PDF document
loader = PyPDFLoader("documents/3.pdf")
pages = loader.load_and_split()

# Create vector store
vectorstore = DocArrayInMemorySearch.from_documents(pages, embedding=embeddings)

# Initialize retriever
retriever = vectorstore.as_retriever()

# Define chain with prompt, model, and parser
parser = StrOutputParser()
chain = (
    {
        "context": itemgetter("question") | retriever,
        "question": itemgetter("question"),
    }
    | prompt
    | model
    | parser
)

# %%
parser = StrOutputParser()
chain = (
    {
        "context": itemgetter("question") | retriever,
        "question": itemgetter("question"),
    }
    | prompt
    | model
    | parser
)

# %%
llm_response = chain.invoke({"question":"Extract the following information from the software architecture document and provide the details in the specified JSON structure "})


# %%
print(llm_response)

# %%
# Function to evaluate a document
def evaluate_document(document_path):
    loader = PyPDFLoader(document_path)
    pages = loader.load_and_split()
    document_content = "\n".join([page.page_content for page in pages])
    
    # Use the rule-based system for initial evaluation
    rule_based_scores = evaluate_document_rule_based(document_content)
    
    # Combine rule-based scores with LLM evaluation if needed
    question = "Evaluate the document based on sustainability criteria."
    context = document_content
    llm_response = chain.invoke({"context": context, "question": question})
    
    return rule_based_scores, llm_response

# %%
# Example usage
document_path = "2.pdf"
rule_based_result, llm_result = evaluate_document(document_path)
print("Rule-Based Result:", rule_based_result)
print("LLM Result:", llm_result)


