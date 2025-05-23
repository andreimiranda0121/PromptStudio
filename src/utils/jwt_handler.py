import jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"

def create_jwt(email: str):
    payload = {
        "sub": email,
        "exp": datetime.utcnow() + timedelta(minutes=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


