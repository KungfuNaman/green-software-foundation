from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.embeddings.bedrock import BedrockEmbeddings
from langchain_community.llms.ollama import Ollama
from dotenv import load_dotenv
import os
import requests
from tenacity import retry, wait_fixed, stop_after_attempt

load_dotenv()
HF_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
LLM_MODEL = os.getenv("LLM_MODEL")

# dim = 384
EMD_MODEL_ID = "sentence-transformers/all-MiniLM-L6-v2"
# dim = 768
# EMD_MODEL_ID = "sentence-transformers/distilbert-base-nli-mean-tokens"

EXT_MODEL_ID = "meta-llama/Llama-2-7b-chat-hf"
# EXT_MODEL_ID = "meta-llama/Llama-2-13b-hf"
# EXT_MODEL_ID = "openai-community/gpt2"
# EXT_MODEL_ID = "deepset/roberta-base-squad2"
# EXT_MODEL_ID = "meta-llama/Llama-2-7b"

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

class Embedder:
    def __init__(self):
        self.model = EMD_MODEL_ID
        self.api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{self.model}"
        self.headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        self.wait = False

    def embed(self, texts):
        """
        Get embedding from HTTP POST query to hugging face inference api
        :param texts: list of texts, num = n
        :return: embeddings, shape = (n, 384)
        """
        response = requests.post(self.api_url, headers=self.headers, json={"inputs": texts, "options": {"wait_for_model": self.wait}})
        embeddings = response.json()
        return embeddings

    def embed_documents(self, text):
        return self.embed(text)

    def embed_query(self, query):
        return self.embed(query)


class Extractor:
    def __init__(self, run_local: bool):
        self.run_local = run_local
        self.wait = False
        if self.run_local:
            self.model = Ollama(model=LLM_MODEL, temperature=0.8,
                                template="""{{ if .System }}<|system|>
                                            {{ .System }}<|end|>
                                            {{ end }}{{ if .Prompt }}<|user|>
                                            {{ .Prompt }}<|end|>
                                            {{ end }}<|assistant|>
                                            {{ .Response }}<|end|>""",
                                system=PROMPT)
        else:
            self.model = EXT_MODEL_ID
            self.api_url = f"https://api-inference.huggingface.co/models/{self.model}"
            self.headers = {"Authorization": f"Bearer {HF_TOKEN}"}

    @retry(wait=wait_fixed(5), stop=stop_after_attempt(10))
    def query(self, payload):
        response = requests.post(self.api_url, headers=self.headers, json=payload)
        return response.json()

    def generate_answer(self, question, context=''):
        if self.run_local:
            response_text = self.model.invoke(question)
            return response_text
        else:
            # payload = {
            #     "inputs": {
            #         "question": question,
            #         "context": context,
            #     }
            # }
            payload = {"inputs": question, "options": {"wait_for_model": self.wait}}
            response = self.query(payload)
            if isinstance(response, list) and len(response) > 0 and 'generated_text' in response[0]:
                response_text = response[0]['generated_text']
                return response_text
            else:
                raise ValueError("Query output format is incorrect: \n" + str(response))


if __name__ == "__main__":
    # t = [
    #     "How do I get a replacement Medicare card?",
    #     "How do I get a replacement card?",
    #     ]
    # embedder = Embedder()
    # output = embedder.embed(t)
    # print(output)
    # print('item: ', len(output))
    # print('dimension: ', len(output[0]))
    # print('='*50)

    q = "can you tell me which and how many servers are used?"
    ct = """
    Human:
Answer the question based only on the following context:

**6.** **Process View**

There’s only one process to take into account. The J2EE model automatically handles threads which are instances of
this process.

Confidential Ó Yummy Inc, 2024 Page 13 of 17


-----

|Sample Software Architecture Document (version 0.7)|Col2|
|---|---|


**7.** **Deployment View**

**Global Overview**

![3.pdf-13-0.png](3.pdf-13-0.png)

**Detailed deployment model with clustering**

-  One IBM HTTP Server will dispatch requests to two different IBM WebSphere servers (load balancing +
clustering)

-  An IBM DB2 Database stores all the information related to online orders

Confidential Ó Yummy Inc, 2024 Page 14 of 17


-----

|Sample Software Architecture Document (version 0.7)|Col2|
|---|---|


![3.pdf-14-0.png](3.pdf-14-0.png)

**8.** **Implementation View**

---

**Deployment view**

**Audience** : Deployment managers.
**Area** : Topology: describes the mapping of the software onto the hardware and shows the system's
distributed aspects.
**Related Artifacts** : Deployment model.

**Use Case view**

**Audience** : all the stakeholders of the system, including the end-users.
**Area** : describes the set of scenarios and/or use cases that represent some significant, central functionality of
the system.
**Related Artifacts** : Use-Case Model, Use-Case documents

**Data view (optional)**

**Audience** : Data specialists, Database administrators
**Area** : Persistence: describes the architecturally significant persistent elements in the data model
**Related Artifacts** : Data model.

Confidential Ó Yummy Inc, 2024 Page 6 of 17


-----

---

**11.** **Quality**

As far as the online catering application is concerned, the following quality goals have been identified:

**Scalability** :

-  **Description** : System’s reaction when user demands increase

-  **Solution** : J2EE application servers support several workload management techniques

**Reliability** , **Availability** :

-  **Description** : Transparent failover mechanism, mean-time-between-failure

-  **Solution :** : J2EE application server supports load balancing through clusters

**Portability** :

-  **Description** : Ability to be reused in another environment

-  **Solution :** The system me be fully J2EE compliant and thus can be deploy onto any J2EE
application server

**Security** :

-  **Description** : Authentication and authorization mechanisms

---

-----

|Sample Software Architecture Document (version 0.7)|Col2|
|---|---|


Each layer has specific responsibilities.

-  The **presentation layer** deals with the presentation logic and the pages rendering

-  The **control layer** manages the access to the domain layer

-  The **resource layer** (integration layer) is responsible for the access to the enterprise information system
(databases or other sources of information)

-  The **domain layer** is related to the business logic and manages the accesses to the resource layer.

-  The **Common Elements** **layer** gathers the common objects reused through all the layers

---

.

_8.2.5_ _Common Elements Layer_

The Common Element layer contains the components re-used within several layers.

**9.** **Data View**

The key data elements related to the online catering system are:

![3.pdf-15-0.png](3.pdf-15-0.png)

**10.** **Size and Performance**

Volumes:

-  Estimated online orders : 100 a day, with peaks in the evening

-  Yummy Inc registered individual customer : about 150

-  Yummy Inc corporate customers : about 100

Performance:

-  Time to process and online payment (credit card validation + confirmation) : less that 10 seconds required

Confidential Ó Yummy Inc, 2024 Page 16 of 17


-----

|Sample Software Architecture Document (version 0.7)|Col2|
|---|---|


**11.** **Quality**

---

Answer the question based on the above context: can you tell me which and how many servers are used   ?

"""

    extractor = Extractor(run_local=False)
    output = extractor.generate_answer(q)
    print('>'*20)
    print(output)
    print('<'*20)
