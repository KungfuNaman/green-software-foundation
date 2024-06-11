# Import necessary libraries
import os
from dotenv import load_dotenv
import json
from langchain_community.llms import Ollama
from langchain_openai.chat_models import ChatOpenAI
from langchain_community.embeddings import OllamaEmbeddings
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import DocArrayInMemorySearch

# Load environment variables
load_dotenv()

# Set API key and model
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = "llama2"  # Change model here if needed

# Initialize model and embeddings based on the model type
if MODEL.startswith("gpt"):
    model = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model=MODEL)
    embeddings = OpenAIEmbeddings()
else:
    model = Ollama(model=MODEL)
    embeddings = OllamaEmbeddings(model=MODEL)

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

# Define function to create vector database
def create_vector_database(document_path):
    # Load and split PDF document
    loader = PyPDFLoader(document_path)
    pages = loader.load_and_split()
    
    # Create vector store
    vectorstore = DocArrayInMemorySearch.from_documents(pages, embedding=embeddings)
    
    return vectorstore

# Define function to generate structured data using the LLM
def generate_response(vectorstore):
    # Initialize retriever
    retriever = vectorstore.as_retriever()
    
    # Combine context from retriever
    context = "\n".join([doc.page_content for doc in vectorstore.documents])
    
    # Define chain with prompt, model, and parser
    parser = StrOutputParser()
    chain = (
        {
            "context": retriever,
        }
        | prompt
        | model
        | parser
    )
    
    # Invoke chain and parse response
    llm_response = chain.invoke({"context": context})
    
    return json.loads(llm_response)

# Example usage
document_path = "documents/3.pdf"
vectorstore = create_vector_database(document_path)
structured_data = generate_response(vectorstore)
print("Structured Data:", json.dumps(structured_data, indent=2))
