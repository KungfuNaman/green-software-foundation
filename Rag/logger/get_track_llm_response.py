import csv
import os

from dotenv import load_dotenv
load_dotenv()

CSV_FILE_PATH = os.getenv("LLM_RESPONSE_LOGGER")



def append_to_csv(
     query, context, search_time, response, response_time, db_time,similarity_results
):
    header = [
        "query",
        "context_text",
        "context_time_ms",
        "response_text",
        "response_time_ms",
        "db_time_ms",
        "similarity_results"
    ]
    row = [query, context, search_time, response, response_time, db_time,similarity_results]

    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(CSV_FILE_PATH), exist_ok=True)

        file_exists = os.path.isfile(CSV_FILE_PATH)

        with open(CSV_FILE_PATH, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if not file_exists:  # If file does not exist, write the header
                writer.writerow(header)
            writer.writerow(row)
    except IOError as e:
        print(f"An error occurred while writing to the CSV file: {e}")

