import requests
import logging
import os
from dotenv import load_dotenv
import json
load_dotenv()

API_URL = os.getenv("API_URL")

def chat_request(email, prompt_id, model, temp, top_p, prompt, use_context, user_input, file=None):
    url = f"{API_URL}/prompt/chat_request/"
    
    # This is the actual Pydantic payload encoded as string
    payload = {
        "email": email,
        "prompt_id": prompt_id,
        "input": user_input,
        "model": model,
        "temperature": temp,
        "top_p": top_p,
        "prompt_template": prompt,
        "use_context": use_context
    }

    form_data = {
        "prompt_settings": json.dumps(payload)  # send as string!
    }

    try:
        if file:
            response = requests.post(url=url, data=form_data, files=file)
        else:
            response = requests.post(url=url, data=form_data)

        if response.status_code == 200:
            return response.json()
        else:
            logging.error(f"API Error: {response.status_code} - {response.text}")
            return {"error": response.status_code, "message": response.text}
    except Exception as e:
        logging.error(f"Request failed: {e}")
        return {"error": "request_failed", "message": str(e)}

