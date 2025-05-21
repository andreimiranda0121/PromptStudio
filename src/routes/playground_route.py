from fastapi import APIRouter, File, UploadFile

router = APIRouter(
    prefix="/prompt",
    tags=['Prompt Playground']
)


@router.post("/saved_settings/")
async def saved_settings(model_settings: str, File):
    return {"test": model_settings}