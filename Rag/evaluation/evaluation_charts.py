import json
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
from tabulate import tabulate
from sklearn.metrics import confusion_matrix


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

    # Separate Results_R-C* and Results_R-M*
    results_r_c_g_ft = []
    results_r_m_g_ft = []
    results_r_e_g_ft = []
    results_r_c_g = []
    results_r_m_g = []
    results_r_e_g = []


    for key, value in data.items():
        if key.startswith("Results_R-C_G-FT"):
            results_r_c_g_ft.extend(value)
        elif key.startswith("Results_R-M_G-FT"):
            results_r_m_g_ft.extend(value)
        elif key.startswith("Results_R-E_G-FT"):
            results_r_e_g_ft.extend(value)
        elif key.startswith("Results_R-C_G"):
            results_r_c_g.extend(value)
        elif key.startswith("Results_R-M_G"):
            results_r_m_g.extend(value)
        elif key.startswith("Results_R-E_G"):
            results_r_e_g.extend(value)

    # Calculate accuracy
    accuracy_r_c_g_ft = calculate_accuracy(results_r_c_g_ft)
    accuracy_r_m_g_ft = calculate_accuracy(results_r_m_g_ft)
    accuracy_r_e_g_ft = calculate_accuracy(results_r_e_g_ft)
    accuracy_r_c_g = calculate_accuracy(results_r_c_g)
    accuracy_r_m_g = calculate_accuracy(results_r_m_g)
    accuracy_r_e_g = calculate_accuracy(results_r_e_g)


    # Plotting the bar graph
    labels = [
        "Results_R-C_G-FT",
        "Results_R-M_G-FT",
        "Results_R-E_G-FT",
        "Results_R-C_G",
        "Results_R-M_G",
        "Results_R-E_G"

    ]
    accuracies = [
        accuracy_r_c_g_ft,
        accuracy_r_m_g_ft,
        accuracy_r_e_g_ft,
        accuracy_r_c_g,
        accuracy_r_m_g,
        accuracy_r_e_g
    ]

    plt.figure(figsize=(10, 5))
    plt.bar(labels, accuracies, color=["blue", "green", "yellow", "red","orange","pink"],width=0.4)
    plt.xlabel("Results")
    plt.ylabel("Accuracy (%)")
    plt.title("Accuracy Comparison")
    plt.ylim(0, 100)

    for i, acc in enumerate(accuracies):
        plt.text(i, acc + 1, f"{acc:.2f}%", ha="center")

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

    results_r_c_g_ft = []
    results_r_m_g_ft = []
    results_r_e_g_ft = []
    results_r_c_g = []
    results_r_m_g = []
    results_r_e_g = []

    for key, value in data.items():
        if key.startswith("Results_R-C_G-FT"):
            results_r_c_g_ft.extend(value)
        elif key.startswith("Results_R-M_G-FT"):
            results_r_m_g_ft.extend(value)
        elif key.startswith("Results_R-E_G-FT"):
            results_r_e_g_ft.extend(value)
        elif key.startswith("Results_R-C_G"):
            results_r_c_g.extend(value)
        elif key.startswith("Results_R-M_G"):
            results_r_m_g.extend(value)
        elif key.startswith("Results_R-E_G"):
            results_r_e_g.extend(value)

    # Calculate metrics
    precision_r_c_g_ft, recall_r_c_g_ft, f1_r_c_g_ft = calculate_metrics(
        results_r_c_g_ft
    )
    precision_r_m_g_ft, recall_r_m_g_ft, f1_r_m_g_ft = calculate_metrics(
        results_r_m_g_ft
    )
    precision_r_e_g_ft, recall_r_e_g_ft, f1_r_e_g_ft = calculate_metrics(
        results_r_e_g_ft
    )
    precision_r_c_g, recall_r_c_g, f1_r_c_g = calculate_metrics(results_r_c_g)
    precision_r_m_g, recall_r_m_g, f1_r_m_g = calculate_metrics(results_r_m_g)
    precision_r_e_g, recall_r_e_g, f1_r_e_g = calculate_metrics(results_r_e_g)

    # Create a table using tabulate
    table = [
        ["Results_R-C_G-FT", precision_r_c_g_ft, recall_r_c_g_ft, f1_r_c_g_ft],
        ["Results_R-M_G-FT", precision_r_m_g_ft, recall_r_m_g_ft, f1_r_m_g_ft],
        ["Results_R-E_G-FT", precision_r_e_g_ft, recall_r_e_g_ft, f1_r_e_g_ft],
        ["Results_R-C_G", precision_r_c_g, recall_r_c_g, f1_r_c_g],
                ["Results_R-M_G", precision_r_m_g, recall_r_m_g, f1_r_m_g],
        ["Results_R-E_G", precision_r_e_g, recall_r_e_g, f1_r_e_g],

    ]

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

    results_r_c_g_ft = []
    results_r_m_g_ft = []
    results_r_e_g_ft = []
    results_r_c_g = []
    results_r_m_g = []
    results_r_e_g = []

    for key, value in data.items():
        if key.startswith("Results_R-C_G-FT"):
            results_r_c_g_ft.extend(value)
        elif key.startswith("Results_R-M_G-FT"):
            results_r_m_g_ft.extend(value)
        elif key.startswith("Results_R-E_G-FT"):
            results_r_e_g_ft.extend(value)
        elif key.startswith("Results_R-C_G"):
            results_r_c_g.extend(value)
        elif key.startswith("Results_R-M_G"):
            results_r_m_g.extend(value)
        elif key.startswith("Results_R-E_G"):
            results_r_e_g.extend(value)

    # Calculate confusion matrices
    confusion_matrix_r_c_g_ft, y_true_r_c_g_ft, y_pred_r_c_g_ft = calculate_confusion_matrix(results_r_c_g_ft)
    confusion_matrix_r_m_g_ft, y_true_r_m_g_ft, y_pred_r_m_g_ft = calculate_confusion_matrix(results_r_m_g_ft)
    confusion_matrix_r_e_g_ft, y_true_r_e_g_ft, y_pred_r_e_g_ft = calculate_confusion_matrix(results_r_e_g_ft)
    confusion_matrix_r_c_g, y_true_r_c_g, y_pred_r_c_g = calculate_confusion_matrix(results_r_c_g)
    confusion_matrix_r_m_g, y_true_r_m_g, y_pred_r_m_g = calculate_confusion_matrix(results_r_m_g)
    confusion_matrix_r_e_g, y_true_r_e_g, y_pred_r_e_g = calculate_confusion_matrix(results_r_e_g)



    # Get the unique labels for dynamic indexing
    labels_r_c_g_ft = sorted(set(y_true_r_c_g_ft + y_pred_r_c_g_ft))
    labels_r_m_g_ft = sorted(set(y_true_r_m_g_ft + y_pred_r_m_g_ft))
    labels_r_e_g_ft = sorted(set(y_true_r_e_g_ft + y_pred_r_e_g_ft))
    labels_r_c_g = sorted(set(y_true_r_c_g + y_pred_r_c_g))
    labels_r_m_g = sorted(set(y_true_r_m_g + y_pred_r_m_g))
    labels_r_e_g = sorted(set(y_true_r_e_g + y_pred_r_e_g))


    # Convert confusion matrices to DataFrame for better visualization
    df_confusion_matrix_r_c_g_ft = pd.DataFrame(confusion_matrix_r_c_g_ft, index=[f"True {label}" for label in labels_r_c_g_ft], columns=[f"Predicted {label}" for label in labels_r_c_g_ft])
    df_confusion_matrix_r_m_g_ft = pd.DataFrame(confusion_matrix_r_m_g_ft, index=[f"True {label}" for label in labels_r_m_g_ft], columns=[f"Predicted {label}" for label in labels_r_m_g_ft])
    df_confusion_matrix_r_e_g_ft = pd.DataFrame(confusion_matrix_r_e_g_ft, index=[f"True {label}" for label in labels_r_e_g_ft], columns=[f"Predicted {label}" for label in labels_r_e_g_ft])
    df_confusion_matrix_r_c_g = pd.DataFrame(confusion_matrix_r_c_g, index=[f"True {label}" for label in labels_r_c_g], columns=[f"Predicted {label}" for label in labels_r_c_g])
    df_confusion_matrix_r_m_g = pd.DataFrame(confusion_matrix_r_m_g, index=[f"True {label}" for label in labels_r_m_g], columns=[f"Predicted {label}" for label in labels_r_m_g])
    df_confusion_matrix_r_e_g  = pd.DataFrame(confusion_matrix_r_e_g , index=[f"True {label}" for label in labels_r_e_g ], columns=[f"Predicted {label}" for label in labels_r_e_g ])

    # Display the confusion matrices using tabulate
    print("Confusion Matrix for Results_R-C_G-FT:")
    print(tabulate(df_confusion_matrix_r_c_g_ft, headers='keys', tablefmt='grid'))

    print("\nConfusion Matrix for Results_R-M_G-FT:")
    print(tabulate(df_confusion_matrix_r_m_g_ft, headers='keys', tablefmt='grid'))

    print("\nConfusion Matrix for Results_R-E_G-FT:")
    print(tabulate(df_confusion_matrix_r_e_g_ft, headers='keys', tablefmt='grid'))

    print("\nConfusion Matrix for Results_R-C_G:")
    print(tabulate(df_confusion_matrix_r_c_g, headers='keys', tablefmt='grid'))

    print("\nConfusion Matrix for Results_R-M_G:")
    print(tabulate(df_confusion_matrix_r_c_g, headers='keys', tablefmt='grid'))

    print("\nConfusion Matrix for Results_R-E_G:")
    print(tabulate(df_confusion_matrix_r_c_g, headers='keys', tablefmt='grid'))




# f1_score_rag_pipeline()
confusion_matrix_rag_settings()
# ragSettings_accuracyChart()

