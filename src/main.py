from fastapi import FastAPI
from src.routes.auth_route import router as auth_router
import uvicorn

app = FastAPI(
    title="StudyPal",
    description="Students upload textbooks, notes, and get flashcards, quizzes, or summaries.",
    version="1.0.0"
)


app.include_router(auth_router)

@app.get("/", tags=['test'])
async def root():
    return {"message": "Hello Welcome to the StudyPal"}

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="localhost", port=8000, reload=True)