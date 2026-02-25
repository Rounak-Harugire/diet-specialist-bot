import os
from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory
from dotenv import load_dotenv

load_dotenv()

def get_chat_history(session_id: str):
    return MongoDBChatMessageHistory(
        connection_string=os.getenv("MONGO_URI"),
        session_id=session_id,
        database_name="diet_chatbot",
        collection_name="history",
    )