from fastapi import FastAPI
from src.routes.auth_route import router as auth_router
from src.routes.playground_route import router as playground_router
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="PromptStudio",
    description="User will create their own customizable prompt settings and model settings",
    version="1.0.0"
)

# Allow Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)
app.include_router(playground_router)

@app.get("/", tags=['test'])
async def root():
    return {"message": "Hello Welcome to the PromptStudio"}

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="localhost", port=8000, reload=True)