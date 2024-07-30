import json
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
from tabulate import tabulate
from sklearn.metrics import confusion_matrix
import re
from collections import defaultdict

RESULTS_JSON_PATH = "frontend/src/api_results/evaluation/results.json"


def preprocess_data(data):
    for key, value in data.items():
        for item in value:
            if item['humanJudgement'] == 'Not Applicable':
                item['humanJudgement'] = 'No'
            if item['llmJudgement'] == 'Not Applicable':
                item['llmJudgement'] = 'No'
    return data


def ragSettings_accuracyChart():
    # Load the JSON data
    with open(RESULTS_JSON_PATH) as f:
        data = json.load(f)
    # Preprocess the data
    data = preprocess_data(data)

    def calculate_accuracy(results):
        total = len(results)
        correct_predictions = sum(
            1 for item in results if item["humanJudgement"] == item["llmJudgement"]
        )
        return (correct_predictions / total) * 100 if total > 0 else 0

    # List of relevant prefixes
    prefixes = [
        'Results_R-C_G_phi3_P2',
        'Results_R-C_G-FT1_phi-3-3.0_P3',
        'Results_R-C_G-FT2_phi-3-4.0_P3',
        'Results_R-C_G-FT3_phi-3-5.0_P3',
        'Results_R-C_G-FT4_phi-3-6.0_P3',
        'Results_R-C_G-FT5_phi-3-7.0-10epoch_P3',
        'Results_R-C_G-FT6_phi-3-30epoch_P3',
        'Results_R-C_G-FT7_phi-3-10epoch_sum_P3',
        'Results_R-C_G-FT'
    ]

    # Dynamically create a dictionary to hold aggregated results
    results_dict = defaultdict(list)
    
    for key, value in data.items():
        for prefix in prefixes:
            if key.startswith(prefix):
                results_dict[prefix].extend(value)
                break

    # Calculate accuracies
    accuracies = []
    for prefix in prefixes:
        accuracy = calculate_accuracy(results_dict[prefix])
        accuracies.append(accuracy)
        print(f"Accuracy for {prefix}: {accuracy:.2f}%")

    # Plotting the bar graph
    plt.figure(figsize=(10, 5))
    plt.bar(prefixes, accuracies, color=["blue", "green", "yellow", "red", "orange", "pink", "black", "purple", "cyan"], width=0.4)
    plt.xlabel("Results")
    plt.ylabel("Accuracy (%)")
    plt.title("Accuracy Comparison")
    plt.ylim(0, 100)

    for i, acc in enumerate(accuracies):
        plt.text(i, acc + 1, f"{acc:.2f}%", ha="center")

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


def f1_score_rag_pipeline():

    # Load the JSON data
    with open(RESULTS_JSON_PATH) as f:
        data = json.load(f)
    # Preprocess the data
    data = preprocess_data(data)

    def calculate_metrics(results):
        y_true = [item["humanJudgement"] for item in results]
        y_pred = [item["llmJudgement"] for item in results]

        precision = (
            precision_score(y_true, y_pred, average="macro", zero_division=0) * 100
        )
        recall = recall_score(y_true, y_pred, average="macro", zero_division=0) * 100
        f1 = f1_score(y_true, y_pred, average="macro", zero_division=0) * 100

        return precision, recall, f1

     # List of relevant prefixes
    prefixes = [
        'Results_R-C_G_phi3_P2',
        'Results_R-C_G-FT1_phi-3-3.0_P3',
        'Results_R-C_G-FT2_phi-3-4.0_P3',
        'Results_R-C_G-FT3_phi-3-5.0_P3',
        'Results_R-C_G-FT4_phi-3-6.0_P3',
        'Results_R-C_G-FT5_phi-3-7.0-10epoch_P3',
        'Results_R-C_G-FT6_phi-3-30epoch_P3',
        'Results_R-C_G-FT7_phi-3-10epoch_sum_P3',
        'Results_R-C_G-FT'
    ]

    # Dynamically create a dictionary to hold aggregated results
    results_dict = defaultdict(list)
    
    for key, value in data.items():
        for prefix in prefixes:
            if key.startswith(prefix):
                results_dict[prefix].extend(value)
                break

    # Calculate metrics
    metrics = {}
    for prefix in prefixes:
        precision, recall, f1 = calculate_metrics(results_dict[prefix])
        metrics[prefix] = (precision, recall, f1)
        print(f"Metrics for {prefix}: Precision={precision:.2f}%, Recall={recall:.2f}%, F1 Score={f1:.2f}%")

    # Create a table using tabulate
    table = []
    for prefix in prefixes:
        precision, recall, f1 = metrics[prefix]
        table.append([prefix, precision, recall, f1])

    headers = ["Configuration", "Precision (%)", "Recall (%)", "F1 Score (%)"]
    table_str = tabulate(table, headers, tablefmt="grid")

    # Display the table
    print(table_str)


def confusion_matrix_rag_settings():
    
    # Load the JSON data
    with open(RESULTS_JSON_PATH) as f:
        data = json.load(f)
    
    # Preprocess the data
    data = preprocess_data(data)

    def calculate_confusion_matrix(results):
        y_true = [item['humanJudgement'] for item in results]
        y_pred = [item['llmJudgement'] for item in results]
        
        cm = confusion_matrix(y_true, y_pred)
        return cm, y_true, y_pred

     # Dynamically identify the unique prefixes
    results_dict = {}

 # List of relevant prefixes
    prefixes = [
        'Results_R-C_G_phi3_P2',
        'Results_R-C_G-FT1_phi-3-3.0_P3',
        'Results_R-C_G-FT2_phi-3-4.0_P3',
        'Results_R-C_G-FT3_phi-3-5.0_P3',
        'Results_R-C_G-FT4_phi-3-6.0_P3',
        'Results_R-C_G-FT5_phi-3-7.0-10epoch_P3',
        'Results_R-C_G-FT6_phi-3-30epoch_P3',
        'Results_R-C_G-FT7_phi-3-10epoch_sum_P3',
        'Results_R-C_G-FT'
    ]
    
     # Dynamically create a dictionary to hold aggregated results
    results_dict = defaultdict(list)
    
    for key, value in data.items():
        for prefix in prefixes:
            if key.startswith(prefix):
                results_dict[prefix].extend(value)
                break

    # Calculate confusion matrices
    confusion_matrices = {}
    y_trues = {}
    y_preds = {}
    for result_key, results in results_dict.items():
        cm, y_true, y_pred = calculate_confusion_matrix(results)
        confusion_matrices[result_key] = cm
        y_trues[result_key] = y_true
        y_preds[result_key] = y_pred

    # Convert confusion matrices to DataFrame for better visualization
    df_confusion_matrices = {}
    for result_key, cm in confusion_matrices.items():
        labels = sorted(set(y_trues[result_key] + y_preds[result_key]))
        df_confusion_matrices[result_key] = pd.DataFrame(
            cm, 
            index=[f"True {label}" for label in labels], 
            columns=[f"Predicted {label}" for label in labels]
        )

    # Display the confusion matrices using tabulate
    for result_key, df_cm in df_confusion_matrices.items():
        print(f"Confusion Matrix for {result_key}:")
        print(tabulate(df_cm, headers='keys', tablefmt='grid'))
        print()







f1_score_rag_pipeline()
confusion_matrix_rag_settings()
# ragSettings_accuracyChart()

