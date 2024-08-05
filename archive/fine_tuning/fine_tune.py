from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, BitsAndBytesConfig

from datasets import load_dataset

from trl import SFTTrainer

from jinja2 import Template

import yaml



MODEL_ID = "microsoft/Phi-3-mini-4k-instruct"

NEW_MODEL_NAME = "TinyButMighty"

DATASET_NAME = "macadeliccc/opus_samantha"

SPLIT = "train"

MAX_SEQ_LENGTH = 2048

num_train_epochs = 1

license = "apache-2.0"

username = "fahdmirzac"

learning_rate = 1.41e-5

per_device_train_batch_size = 4

gradient_accumulation_steps = 1



model = AutoModelForCausalLM.from_pretrained(MODEL_ID, trust_remote_code=True)

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True)

dataset = load_dataset("macadeliccc/opus_samantha", split="train")



EOS_TOKEN=tokenizer.eos_token_id



def process_dataset(mydata):

    conversations = mydata["conversations"]

    texts = []

    mapper = {"system": "system\n", "human": "\nuser\n", "gpt": "\nassistant\n"}

    end_mapper = {"system": "", "human": "", "gpt": ""}

    for c in conversations:

        text = "".join(f"{mapper[(turn := x['from'])]} {x['value']}\n{end_mapper[turn]}" for x in c)

        texts.append(f"{text}{EOS_TOKEN}")

    return {"text": texts}



dataset = dataset.map(process_dataset, batched=True)

print(dataset['text'][2])



args = TrainingArguments(

    per_device_train_batch_size=1,

    gradient_accumulation_steps=gradient_accumulation_steps,

    gradient_checkpointing=True,

    learning_rate=2e-5,

    lr_scheduler_type="cosine",

    max_steps=-1,

    num_train_epochs=num_train_epochs,

    save_strategy="no",

    logging_steps=1,

    output_dir=NEW_MODEL_NAME,

    optim="paged_adamw_32bit",

    bf16=True,

)



trainer = SFTTrainer(

    model=model,

    args=args,

    train_dataset=dataset,

    dataset_text_field="text",

    max_seq_length=MAX_SEQ_LENGTH,

    formatting_func=process_dataset

)



trainer.train()