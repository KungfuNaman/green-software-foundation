import json

with open('sample_results.json', 'r') as file:
    data = json.load(file)

def remove_keys(d, keys):
    for key in keys:
        if key in d:
            del d[key]

def rename_keys(d, key_map):
    for old_key, new_key in key_map.items():
        if old_key in d:
            d[new_key] = d.pop(old_key)

keys_to_remove = ["humanJudgement", "humanExplanation", "ecoDocContext"]

keys_to_rename = {"llmJudgement": "result", "llmExplanation": "explanation"}

for results_set in data:
    for object in data[results_set]:
        remove_keys(object, keys_to_remove)
        rename_keys(object, keys_to_rename)

with open('../../frontend/src/api_results/categories.json', 'r') as categories_file:
    categories = json.load(categories_file)

for results_set in data:
    for object in data[results_set]:
        for object2 in categories["Questions"]:
            if object["query"] == object2["query"]:
                object["type"] = object2["type"]

with open('modified_results.json', 'w') as file:
    json.dump(data, file, indent=4)

