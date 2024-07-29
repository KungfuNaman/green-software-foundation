from huggingface_hub import ModelCard, ModelCardData, HfApi

from jinja2 import Template



template_text = """

---

license: {{ license }}

---



# {{ NEW_MODEL_NAME }}



{{ NEW_MODEL_NAME }} is an SFT fine-tuned version of {{ MODEL_ID }} using a custom training dataset.

This model was made with [Phinetune]()



## Process

- Learning Rate: {{ learning_rate }}

- Maximum Sequence Length: {{ MAX_SEQ_LENGTH }}

- Dataset: {{ DATASET_NAME }}

- Split: {{ SPLIT }}



## 💻 Usage

```python

!pip install -qU transformers

from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline



model = "{{ username }}/{{ NEW_MODEL_NAME }}"

tokenizer = AutoTokenizer.from_pretrained(model)



# Example prompt

prompt = "Your example prompt here"



# Generate a response

model = AutoModelForCausalLM.from_pretrained(model)

pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)


outputs = pipeline(prompt, max_length=50, num_return_sequences=1)

print(outputs[0]["generated_text"])

```



"""

# Create a Jinja template object

jinja_template = Template(template_text.strip())



# Fill the template

content = jinja_template.render(

    license=license,

    NEW_MODEL_NAME=NEW_MODEL_NAME,

    MODEL_ID=MODEL_ID,

    learning_rate=learning_rate,

    MAX_SEQ_LENGTH=MAX_SEQ_LENGTH,

    DATASET_NAME=DATASET_NAME,

    SPLIT=SPLIT,

    username=username,

)



model.save_pretrained(f"{username}/{NEW_MODEL_NAME}")

tokenizer.save_pretrained(f"{username}/{NEW_MODEL_NAME}")



from google.colab import userdata



# Save the model card

card = ModelCard(content)

card.save(f"{username}/{NEW_MODEL_NAME}/README.md")



# Defined in the secrets tab in Google Colab

api = HfApi(token=userdata.get("HF_TOKEN"))



# Upload merge folder

api.create_repo(

    repo_id=f"{username}/{NEW_MODEL_NAME}",

    repo_type="model",

    exist_ok=True,

)



api.upload_folder(

    repo_id=f"{username}/{NEW_MODEL_NAME}",

    folder_path=f"{username}/{NEW_MODEL_NAME}",

)