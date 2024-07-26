import json
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score
from tabulate import tabulate


RESULTS_JSON_PATH = "frontend/src/api_results/evaluation/results.json"


def ragSettings_accuracyChart():
    # Load the JSON data
    with open(RESULTS_JSON_PATH) as f:
        data = json.load(f)

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

    for key, value in data.items():
        if key.startswith("Results_R-C_G-FT"):
            results_r_c_g_ft.extend(value)
        elif key.startswith("Results_R-M_G-FT"):
            results_r_m_g_ft.extend(value)
        elif key.startswith("Results_R-E_G-FT"):
            results_r_e_g_ft.extend(value)
        elif key.startswith("Results_R-C_G"):
            results_r_c_g.extend(value)

    # Calculate accuracy
    accuracy_r_c_g_ft = calculate_accuracy(results_r_c_g_ft)
    accuracy_r_m_g_ft = calculate_accuracy(results_r_m_g_ft)
    accuracy_r_e_g_ft = calculate_accuracy(results_r_e_g_ft)
    accuracy_r_c_g = calculate_accuracy(results_r_c_g)

    # Plotting the bar graph
    labels = [
        "Results_R-C_G-FT",
        "Results_R-M_G-FT",
        "Results_R-E_G-FT",
        "Results_R-C_G",
    ]
    accuracies = [
        accuracy_r_c_g_ft,
        accuracy_r_m_g_ft,
        accuracy_r_e_g_ft,
        accuracy_r_c_g,
    ]

    plt.figure(figsize=(10, 5))
    plt.bar(labels, accuracies, color=["blue", "green", "yellow", "red"])
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

    for key, value in data.items():
        if key.startswith("Results_R-C_G-FT"):
            results_r_c_g_ft.extend(value)
        elif key.startswith("Results_R-M_G-FT"):
            results_r_m_g_ft.extend(value)
        elif key.startswith("Results_R-E_G-FT"):
            results_r_e_g_ft.extend(value)
        elif key.startswith("Results_R-C_G"):
            results_r_c_g.extend(value)

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

    # Create a table using tabulate
    table = [
        ["Results_R-C_G-FT", precision_r_c_g_ft, recall_r_c_g_ft, f1_r_c_g_ft],
        ["Results_R-M_G-FT", precision_r_m_g_ft, recall_r_m_g_ft, f1_r_m_g_ft],
        ["Results_R-E_G-FT", precision_r_e_g_ft, recall_r_e_g_ft, f1_r_e_g_ft],
        ["Results_R-C_G", precision_r_c_g, recall_r_c_g, f1_r_c_g],
    ]

    headers = ["Configuration", "Precision (%)", "Recall (%)", "F1 Score (%)"]
    table_str = tabulate(table, headers, tablefmt="grid")

    # Display the table
    print(table_str)


# ragSettings_accuracyChart()
f1_score_rag_pipeline()
