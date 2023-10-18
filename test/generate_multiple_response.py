import os
from dotenv import load_dotenv
from pymongo import MongoClient
import openai

# Load environment variables from .env file
load_dotenv()
MONGO_DB_URI = os.environ.get('MONGO_DB_URI')
MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# Collection names
MAIN_COLLECTION = 'car_responses1'
EXT_COLLECTION = 'car_ext'

# Initialize OpenAI's API
openai.api_key = OPENAI_API_KEY

def generate_sentences_from_response(response_text):
    initPrompt = ("Create 50 sentences similar to the given sentence in different tone, grammar, etc. "
                  "Separate each sentence with a _#_#_ so that I can identify. "
                  "Just give the text only in the same line, no extra character or response. Only pure data: ")
    
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=initPrompt + response_text,
        max_tokens=1000
    )
    
    # Check if the delimiter exists in the response
    if '_#_#_' not in response.choices[0]['text']:
        print(f"Delimiter not found in response for: {response_text}")
        print(response.choices[0]['text'])
        return []

    # Split the response text based on the delimiter and return the list of sentences
    return response.choices[0]['text'].split('_#_#_')


def extend_responses():
    # Connect to the MongoDB server and get the collections
    client = MongoClient(MONGO_DB_URI)
    db = client[MONGO_DB_NAME]
    responses = db[MAIN_COLLECTION]
    responses_ext = db[EXT_COLLECTION]

    
    # Iterate over each document in the responses collection
    for doc in responses.find():
        original_response = doc['response']
        generated_sentences = generate_sentences_from_response(original_response)

        # Store each generated sentence in responses_ext with a reference to the original ID
        for sentence in generated_sentences:
            if sentence.strip():  # Check if the sentence is not just whitespace
                print(sentence)
                responses_ext.insert_one({
                    'text': sentence.strip(),
                    'reference_id': doc['_id']
                })

    client.close()


# Call the function
if __name__ == "__main__":
    extend_responses()

