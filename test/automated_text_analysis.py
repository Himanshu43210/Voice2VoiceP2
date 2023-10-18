from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv
from faiss_response_mapping_testing import find_most_similar

# Load environment variables from .env file
load_dotenv()
MONGO_DB_URI = os.environ.get('MONGO_DB_URI')
MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME')

# Collection name
MAIN_COLLECTION = 'car_responses1'
EXT_COLLECTION = 'car_ext'

# Connect to MongoDB using the environment variables
client = MongoClient(MONGO_DB_URI)
db = client[MONGO_DB_NAME]

def get_reference_text(reference_id):
    doc = db[MAIN_COLLECTION].find_one({"_id": reference_id})
    return doc.get("response") if doc else None

def process_chunk(chunk):
    for doc in chunk:
        # Get the response content
        input_sentence = doc.get("text", "")
        
        # Call the find_most_similar method
        start_time = datetime.now()
        matched_text, similarity_score = find_most_similar(input_sentence)
        end_time = datetime.now()
        time_taken = (end_time - start_time).total_seconds()
        
        # Update the document
        update_data = {
            "matched_text": matched_text,
            "similarity_score": similarity_score,
            "time_taken": time_taken
        }
        
        # If reference_id is present, fetch the original sentence
        reference_id = doc.get("reference_id")
        if reference_id:
            reference_text = get_reference_text(reference_id)
            if reference_text:
                update_data["reference_text"] = reference_text
        
        db[EXT_COLLECTION].update_one({"_id": doc["_id"]}, {"$set": update_data})


def main():
    CHUNK_SIZE = 50
    skip = 0

    client = MongoClient(MONGO_DB_URI)
    db = client[MONGO_DB_NAME]

    while True:
        chunk = list(db[EXT_COLLECTION].find().skip(skip).limit(CHUNK_SIZE))
        if not chunk:
            break
        process_chunk(chunk)
        skip += CHUNK_SIZE

if __name__ == "__main__":
    main()
