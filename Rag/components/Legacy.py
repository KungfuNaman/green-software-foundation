import os
import pymongo
import pandas as pd

EMBEDDINGS_LOG_DIR = os.getenv("EMBEDDINGS_LOG_DIR")

# def log_embeddings_to_tensorboard(emb_local: bool):
#     # Load Chroma database and get embeddings and metadata
#     db = load_chroma_db(emb_local, db_path=CHROMA_PATH)
#
#     embeddings = db.get(include=["embeddings", "metadatas"])
#     vectors = embeddings["embeddings"]
#     metadata = embeddings["metadatas"]
#
#     # Convert metadata to a pandas DataFrame for easier handling
#     metadata_df = pd.DataFrame(metadata)
#
#     # Select specific metadata columns for TensorBoard
#     columns = ["id", "source"]
#     selected_meta = metadata_df[columns]
#     selected_meta_list = selected_meta.to_numpy().tolist()
#
#     # Prepare TensorBoard writer
#     writer = SummaryWriter(EMBEDDINGS_LOG_DIR)
#
#     # Convert vectors to tensor
#     vectors_tensor = torch.tensor(vectors)
#
#     # Set global step and tag
#     global_step = 1
#     tag = "model1"
#
#     # Define projector config path
#     pbconfig = os.path.join(EMBEDDINGS_LOG_DIR, "projector_config.pbtxt")
#
#     # Read existing projector config entries
#     def read_pbconfig(path):
#         if os.path.exists(path):
#             with open(path, "r") as f:
#                 entries = f.read()
#                 return entries
#         return ""
#
#     old_entries = read_pbconfig(pbconfig)
#
#     # Add embeddings to TensorBoard
#     writer.add_embedding(
#         vectors_tensor,
#         metadata=selected_meta_list,
#         global_step=global_step,
#         metadata_header=columns,
#         tag=tag,
#     )
#
#     writer.close()
#
#     # Write new projector config entries
#     new_entry = read_pbconfig(pbconfig)
#     with open(pbconfig, "w") as f:
#         f.write(old_entries + "\n" + new_entry)
#
#     print(f"Embeddings have been logged to TensorBoard at {EMBEDDINGS_LOG_DIR}")


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
