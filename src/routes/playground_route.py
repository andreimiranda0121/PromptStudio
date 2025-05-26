import os
import tempfile
from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from typing import Optional
from src.database.connection import get_db
from src.services.chain import Chain
from src.models.model import PromptSetting
import json
from datetime import datetime
import uuid

router = APIRouter(
    prefix="/prompt",
    tags=['Prompt Playground']
)

@router.post("/chat_request/")
async def chat_request(
    prompt_settings: str = Form(...), 
    file: Optional[UploadFile] = File(None)
):
    try:
        settings_dict = json.loads(prompt_settings)

        # Save uploaded file if provided
        if file:
            suffix = os.path.splitext(file.filename)[1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(await file.read())
                tmp_file_path = tmp.name
            settings_dict['file_path'] = tmp_file_path
        else:
            tmp_file_path = None

        # Create and run the chain
        chain = Chain(settings_dict)
        user_input = settings_dict.get("input", "")
        if not user_input:
            raise HTTPException(status_code=400, detail="user_input is required")
        
        response = chain.run(user_input)

        # Cleanup file
        if tmp_file_path and os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


# Save settings to prompt history collection
@router.post("/saved_settings/")
async def save_settings(
    email: str = Form(...),
    model_settings: str = Form(...),
):
    db = get_db()
    collection = db['prompt_history']

    try:
        parsed_settings = json.loads(model_settings)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid model_settings JSON")

    # Add timestamp to entry
    parsed_settings["timestamp"] = datetime.utcnow().isoformat()
    # Check if the user already has a history document
    user_doc = collection.find_one({"email": email})
    if not user_doc:
        collection.insert_one({
            "email": email,
            "prompt_history": [parsed_settings]
        })
    else:
        collection.update_one(
            {"email": email},
            {"$push": {"prompt_history": parsed_settings}}
        )

    return {"status": "saved"}

@router.delete("/delete_prompt/")
async def delete_prompt(email: str, prompt_id: str):
    db = get_db()
    collection = db['prompt_history']

    result = collection.update_one(
        {"email": email},
        {"$pull": {"prompt_history": {
            "prompt_id" : prompt_id
        }}}
    )

    if result:
        return {"success": True}
    else:
        return {"sucess": False}

@router.get("/prompt_history")
async def prompt_history(email: str):
    db = get_db()
    collection = db['prompt_history']

    user_doc = collection.find_one({"email": email}, {"_id": 0})
    if not user_doc or not user_doc.get("prompt_history"):
        raise HTTPException(status_code=404, detail="No prompt history found")
    prompt_count = len(user_doc["prompt_history"])
    print(prompt_count)
    return {"history": user_doc["prompt_history"], "prompt_count":prompt_count}
