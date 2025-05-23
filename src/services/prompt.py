from src.database.connection import db
from datetime import datetime

collection = db["prompt_history"]

def save_prompt(user_email: str, prompt_data: dict):
    prompt_data["user_email"] = user_email
    prompt_data["created_at"] = datetime.utcnow()
    prompt_data.pop("use_context", None)  # Remove if accidentally passed
    collection.insert_one(prompt_data)
