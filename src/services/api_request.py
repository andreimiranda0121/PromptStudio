import requests
import logging
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")

def chat_request(email,model,temp,top_p,prompt,use_context):
    url = f"{API_URL}/prompt/chat_request/"
    payload = {
        "model": model,
        "temperature": temp,
        "prompt_template": prompt,
        "use_context": use_context
    }

    response = requests.post(url=url, data=payload)

    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code
