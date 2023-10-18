from pymongo import MongoClient

class MongoDB:
    def __init__(self, db_url, db_name):
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]

    def insert_response(self, text, conversation_id):
        collection = self.db.responses
        document = {
            "_id": conversation_id,  # assuming conversation_id is unique
            "Text": text,
            "conversationId": conversation_id
        }
        collection.insert_one(document)

    def close_connection(self):
        self.client.close()
