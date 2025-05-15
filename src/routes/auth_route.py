from fastapi import APIRouter

router = APIRouter(
    tags=["auth"]
)

@router.get("/auth_home/")
async def home():
    return {"messages": "Welcome to the Authentication API"}