from fastapi import APIRouter, File, UploadFile, Form
from typing import Optional
import json

router = APIRouter(
    prefix="/prompt",
    tags=['Prompt Playground']
)



@router.post("/saved_settings/")
async def save_settings(model_settings: str = Form(...), file: Optional[UploadFile] = File(None)):
    parsed_settings = json.loads(model_settings)
    print(parsed_settings)
    print(type(parsed_settings))
    if file:
        contents = await file.read()
        print(f"Uploaded file name: {file.filename}, size: {len(contents)} bytes")
    return {"status": "saved"}