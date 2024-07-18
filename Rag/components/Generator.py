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
            self.init_local_generator(self.model_name)
        else:
            self.model_hf_id, self.api_url, self.headers, self.wait = None, None, None, None
            self.init_remote_generator()

    def init_local_generator(self, model_name):
        self.model = Ollama(
            model=model_name,
            mirostat_tau=3,             # Default = 5.0
            num_ctx=3072,               # Default = 2048
            repeat_last_n=128,          # Default = 64, 0 = disabled, -1 = num_ctx
            repeat_penalty=1.5,         # Default = 1.1
            temperature=0.4,            # Default = 0.8
            template="",
            top_k=10,                   # Default = 40
            top_p=0.5,                  # Default = 0.9
            verbose=False
        )

    def set_template(self, template):
        """ TODO: Add customized template here"""
        pass

    def set_any_other_param(self):
        """ TODO: Add any other param setting here"""
        pass

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



