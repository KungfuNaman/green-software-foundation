import json
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from collections import defaultdict, Counter

# Use the 'Agg' backend for non-GUI rendering
matplotlib.use('Agg')

def generate_pie_chart(result_path):
    # Load the JSON data from the file
    with open(result_path, 'r') as file:
        data = json.load(file)
    
    # Extracting the categories
    categories = [item['category'] for item in data["response"]]

    # Counting the occurrences of each category
    category_counts = Counter(categories)

    # Define custom colors
    colors = ['#B4DCB4','#ECF2D7','#AEC564','#2E6B68','#0D2528']

    # Creating a pie chart
    plt.figure(figsize=(8, 6))
    wedges, texts, autotexts = plt.pie(
        category_counts.values(), 
        colors=colors, 
        autopct='%1.1f%%', 
        startangle=140, 
        textprops=dict(color="black")
    )

    # Customize the labels' font
    for text in texts:
        text.set_fontsize(12)
        text.set_color('black')
    for autotext in autotexts:
        autotext.set_fontsize(10)
        autotext.set_color('black')

    # Position the legend on the right
    plt.legend(
        wedges, 
        category_counts.keys(), 
        title="Categories", 
        loc="center left", 
        bbox_to_anchor=(1, 0, 0.5, 1),
        fontsize=12
    )

    plt.suptitle('Distribution of Categories in the Dataset', x=0.75, ha='center')
    # Save the figure
    plt.savefig('Charts/PieChart.png', format='png', bbox_inches='tight')
    plt.close()

def generate_bar_chart(result_path):
    # Load the JSON data from the file
    with open(result_path, 'r') as file:
        data = json.load(file)

    # Initialize counters
    judgement_counts = defaultdict(lambda: {'Yes': 0, 'No': 0, 'Not Applicable': 0})

    # Count the judgements for each category
    for item in data["response"]:
        category = item['category']
        judgement = item['result']
        judgement_counts[category][judgement] += 1

    # Extracting the data for plotting
    categories = list(judgement_counts.keys())
    yes_counts = [judgement_counts[category]['Yes'] for category in categories]
    no_counts = [judgement_counts[category]['No'] for category in categories]
    na_counts = [judgement_counts[category]['Not Applicable'] for category in categories]

    # Setting up the bar positions
    x = np.arange(len(categories))
    width = 0.2  # Width of the bars

    # Creating the bar chart
    plt.figure(figsize=(10, 7))
    plt.bar(x - width, yes_counts, width, label='Yes', color='#BEC8A9')
    plt.bar(x, no_counts, width, label='No', color='#AEC564')
    plt.bar(x + width, na_counts, width, label='Not Applicable', color='#0D2528')

    # Adding labels and title
    plt.xlabel('Categories of Green Practices')
    plt.ylabel('No of Practices')
    plt.title('Judgement Distribution by Category')
    plt.xticks(x, categories, ha="center")
    plt.legend()

    # Displaying the bar chart
    plt.tight_layout()
    # Save the figure
    plt.savefig('Charts/BarChart.png', format='png')
    plt.close()

# Enable interactive mode
#plt.ion()


# generate_pie_chart('frontend/src/api_results/evaluation/Phi3_results.json', "Results_R-C_G_phi3_P2_Netflix")
# generate_bar_chart('frontend/src/api_results/evaluation/Phi3_results.json', "Results_R-C_G_phi3_P2_Netflix")