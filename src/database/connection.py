from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

def get_db():
    MONGO_URI = os.getenv("DB_URI")
    client = MongoClient(MONGO_URI)
    
    return client["prompt_studio"]