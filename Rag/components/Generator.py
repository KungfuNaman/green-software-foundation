import os
from langchain_community.llms.ollama import Ollama
import requests
from openai import OpenAI
from tenacity import retry, wait_fixed, stop_after_attempt


class Generator:
    HF_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    def __init__(self, run_local=True, sota_model=False, model_name=os.getenv("LLM_MODEL"), instruction=None):
        self.run_local = run_local
        self.sota_model = sota_model
        self.model = None
        self.instruction = instruction if instruction else self.get_instruction()

        if self.run_local:
            self.model_name = model_name
            self.template = self.get_template()
            self.init_local_generator(self.model_name, self.template, self.instruction)
        elif self.sota_model:
            self.model_name = "gpt-4o-mini"
            self.client = self.init_sota_generator(Generator.OPENAI_API_KEY)
        else:
            self.model_hf_id, self.api_url, self.headers, self.wait = None, None, None, None
            self.init_remote_generator()

    def init_local_generator(self, model_name, template, instruction):
        OLLAMA_URL = os.getenv("OLLAMA_URL")

        self.model = Ollama(
            model=model_name,
            mirostat_tau=5,             # Default = 5.0
            num_ctx=2048,               # Default = 2048
            repeat_last_n=64,          # Default = 64, 0 = disabled, -1 = num_ctx
            repeat_penalty=1.1,         # Default = 1.1
            temperature=0.8,            # Default = 0.8
            top_k=40,                   # Default = 40
            top_p=0.9,                  # Default = 0.9
            verbose=False,
            template=template,
            system=instruction,
            base_url=OLLAMA_URL
        )

    @staticmethod
    def get_instruction():
        instruction = """
        Act as a professional assistant in the field of software development, you need to give precise and short answers 
        to respond to the question that I gave, beside, also give a suggestion that describe the benefits of using this technic mentioned in the question in this software project.\n 
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
        Explanation: <The description of the reason for the judgement above>\n\
        Suggestion: <The benefits of using this technic in this software projects>"\"\n\n
        For Your Answer:\n
        In judgement,\n
        <Yes> means that in the context of my question, there exists a technology or green practice that is relevant to the question.\n
        <No> means that in the context of my question, there is no technology or green practice that is relevant to the question.\n
        <Not Applicable> means that in the context of my question, this application is not applicable to this technique or to the green practice, e.g., applications that need to focus on real-time feedback, such as online games, are not applicable to the green practice of \"cache static data\".\n\n
        In Explanation, you need to explain the judgment you made above in less than 3 sentences.\n\n
		In Suggestion, you need to give suggestion about using this technic in less than 5 sentences.\n\n
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

    @staticmethod
    def init_sota_generator(api_key):
        client = OpenAI(api_key=api_key)
        return client

    def gpt_chat(self, prompt):
        instruction_text = Generator.get_instruction()
        history = [{"role": "system", "content": instruction_text}, {"role": "user", "content": prompt}]
        if self.sota_model and not self.run_local:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=history,
            )
            assistant_answer = completion.choices[0].message.content
            return assistant_answer

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



