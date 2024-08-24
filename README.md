# EcoDoc Sense
## 1. Overview
EcoDoc Sense is a web application that focusing on analysing the compliance of software architecture documents
with certain green software patterns. A sustainability report is generated based on developer’s
software architecture document, highlighting whether green software patterns are being adhered to
or overlooked. Additionally, it provides suggestions on which green patterns should be implemented
in the software. 


## 2. Project Structure
### Backend 
Built out the main RAG ( Retrieval-Augmented Generation ) pipeline for the project 
and uses FastAPI to implement the RESTful service. Code in "Rag" folder.

### Frontend 
Built out a user-friendly web user interface with the React Framework.

### Scripts
The scripts for finetuning the models are included in the "Finetuning" folder.

### Local Tools
Ollama is used as the local LLM launcher in the project.


## 3. Run on Local PC
### Get ready for Ollama
Install [**Ollama**](https://www.ollama.com/) to local machine. After that, pull necessary models.
```bash
# pull Llama2 for embeddings generation
ollama pull llama2

# pull LLaVA for image extraction of user's document
ollama pull llava
```
Download finetuned model for final answer generation [here](https://drive.google.com/file/d/1l1dnbQlQGiQVCTp925pB07Sh3cYnViKR/view?usp=sharing).<br/>
Then, copy the Modelfile in project root directory to where you store the finetuned model.<br/>
After that, create a model instance by Modelfile.
```bash
# create the model instance
ollama create fineTunedModel -f /root/Modelfile
```

### Start backend server
```bash
# change directory
cd .\Rag\

# install dependencies
pip install -r .\requirements.txt

# start server
python .\api.py
```

### Start frontend server
```bash
# change directory
 cd .\frontend\

# install dependencies
npm install

# start server
npm start
```
Now EcoDoc Sense is ready on **http://localhost:3000/**


## 4. Run with Docker
Install [**Docker Desktop**](https://www.docker.com/products/docker-desktop/) to your machine. <br>
Use the command below to create the docker image and run locally.
```bash
# build the docker image and run
docker-compose up --build
```
