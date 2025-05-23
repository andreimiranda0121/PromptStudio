from fastapi import APIRouter, File, UploadFile, Form
from typing import Optional
from src.database.connection import get_db
import json

router = APIRouter(
    prefix="/prompt",
    tags=['Prompt Playground']
)



@router.post("/saved_settings/")
async def save_settings(
    email: str = Form(...),
    model_settings: str = Form(...),
    file: Optional[UploadFile] = File(None)
):
    db = get_db()
    collection = db['model_settings']

    parsed_settings = json.loads(model_settings)

    user_doc = collection.find_one({"email": email})
    if not user_doc:
        collection.insert_one({
            "email": email,
            "model_settings": parsed_settings
        })
    else:
        collection.update_one(
            {"email": email},
            {"$set": {"model_settings": parsed_settings}}
        )

    if file:
        contents = await file.read()
        # Optional: Save to GridFS or base64 encode and store inline

    return {"status": "saved"}
