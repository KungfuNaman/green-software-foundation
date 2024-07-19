import os
from langchain_community.llms.ollama import Ollama
import requests
from tenacity import retry, wait_fixed, stop_after_attempt


class Generator:
    HF_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

    def __init__(self, run_local=True, model_name=os.getenv("LLM_MODEL")):
        self.run_local = run_local
        self.model = None

        if self.run_local:
            self.model_name = model_name
            self.template, self.instruction = self.get_template(), self.get_instruction()
            self.init_local_generator(self.model_name, self.template, self.instruction)
        else:
            self.model_hf_id, self.api_url, self.headers, self.wait = None, None, None, None
            self.init_remote_generator()

    def init_local_generator(self, model_name, template, instruction):
        self.model = Ollama(
            model=model_name,
            mirostat_tau=3,             # Default = 5.0
            num_ctx=3072,               # Default = 2048
            repeat_last_n=128,          # Default = 64, 0 = disabled, -1 = num_ctx
            repeat_penalty=1.5,         # Default = 1.1
            temperature=0.8,            # Default = 0.8
            top_k=10,                   # Default = 40
            top_p=0.5,                  # Default = 0.9
            verbose=False,
            template=template,
            system=instruction
        )

    @staticmethod
    def get_instruction():
        instruction = """
        Act as a professional assistant in the field of software development, you need to give precise and short answers 
        to respond to the question that I gave.\n 
        I will take the corresponding text snippet from the design file of the software development, and you need to use 
        a certain format and \"yes/no/not applicable\" to answer the question.
        \n\n My Input would be:\n\"\"\n
        Answer the question based only on the following context:
        \n<context>\n\nQuestion:\n<question>\n\"\"\n\n
        For My Input:\n
        <context>: Five paragraphs excerpted from my design document for software development.\n
        <question>: I'll ask you if this uses a certain technology to support a certain green practice. 
        \n\n Your Answer must adhere to this format:\n\"\"\n
        Response:\nJudgement: Print <Yes> / <No> / <Not Applicable> only.\n
        Explanation: <The description of the reason for the judgement above>\n\"\"\n\n
        For Your Answer:\n
        In judgement,\n
        <Yes> means that in the context of my question, there exists a technology or green practice that is relevant to the question.\n
        <No> means that in the context of my question, there is no technology or green practice that is relevant to the question.\n
        <Not Applicable> means that in the context of my question, this application is not applicable to this technique or to the green practice, e.g., applications that need to focus on real-time feedback, such as online games, are not applicable to the green practice of \"cache static data\".\n\n
        In Explanation, you need to explain the judgment you made above in less than 3 sentences.\n\n
        """
        return instruction

    @staticmethod
    def get_template():
        template = """
        {{ if .System }}<|system|>
        {{ .System }}<|end|>
        {{ end }}{{ if .Prompt }}<|user|>
        {{ .Prompt }}<|end|>
        {{ end }}<|assistant|>
        {{ .Response }}<|end|>
        """
        return template

    def init_remote_generator(self):
        self.model_hf_id = "meta-llama/Llama-2-7b-chat-hf"
        # model_hf_id = "meta-llama/Llama-2-13b-hf"
        # model_hf_id = "openai-community/gpt2"
        # model_hf_id = "deepset/roberta-base-squad2"
        # model_hf_id = "meta-llama/Llama-2-7b"

        self.api_url = f"https://api-inference.huggingface.co/models/{self.model_hf_id}"
        self.headers = {"Authorization": f"Bearer {Generator.HF_TOKEN}"}
        self.wait = False

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



