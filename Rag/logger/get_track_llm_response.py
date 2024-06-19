import csv
import os
import pymongo
import pandas as pd

from dotenv import load_dotenv

load_dotenv()

CSV_FILE_PATH = os.getenv("LLM_RESPONSE_LOGGER")
# Add the parent directory to the Python path


def append_to_csv(
    query, context, search_time, response, response_time, db_time, similarity_results
):
    """add data to local csv and mongo cloud"""
    header = [
        "query",
        "context_text",
        "context_time_ms",
        "response_text",
        "response_time_ms",
        "db_time_ms",
        "similarity_results",
    ]
    row = [
        query,
        context,
        search_time,
        response,
        response_time,
        db_time,
        similarity_results,
    ]

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
        # add_to_mongo(query,context,search_time,response,response_time,db_time,similarity_results)

def add_to_mongo(query,context,search_time,response,response_time,db_time,similarity_results):
    try:
        collection = get_mongo_collection()
        document = {
            "query": query,
            "context_text": context,
            "context_time_ms": search_time,
            "response_text": response,
            "response_time_ms": response_time,
            "db_time_ms": db_time,
            "similarity_results": serialize_document(similarity_results),
        }

        try:
            # Insert the document into the MongoDB collection
            collection.insert_one(document)
            print("Document inserted successfully.")
        except pymongo.errors.PyMongoError as e:
            print(f"An error occurred while inserting the document into MongoDB: {e}")
    except Exception as e:
        print(f"An error occurred while interacting with MongoDB: {e}")

MONGO_STRING = os.getenv("MONGO_STRING")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")
MONGO_DATABASE = os.getenv("MONGO_DATABASE")


def get_mongo_collection():
    """Set up and return the MongoDB collection"""
    client = pymongo.MongoClient(MONGO_STRING)
    db = client[MONGO_DATABASE]
    collection = db[MONGO_COLLECTION]
    return collection


def serialize_document(documents):
    obj = {}
    obj["meta_data"] = [doc.metadata.get("id", None) for doc, _score in documents]
    return obj


def convert_data_to_csv():
    collection = get_mongo_collection()
    # Query all documents in the collection
    documents = list(collection.find())

    # Create a DataFrame from the documents
    df = pd.DataFrame(documents)

    # Export DataFrame to CSV
    df.to_csv("gsf_export.csv", index=False)


def import_csv_to_mongo(csv_file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Convert the DataFrame to a list of dictionaries
    data = df.to_dict(orient="records")

    # Get the MongoDB collection
    collection = get_mongo_collection()

    # Insert the list of dictionaries into the MongoDB collection
    if data:
        collection.insert_many(data)
        print(f"Inserted {len(data)} documents into the collection.")
    else:
        print("No data found in the CSV file.")


# import_csv_to_mongo("Rag/logger/llmResponse.csv")
# convert_data_to_csv()
