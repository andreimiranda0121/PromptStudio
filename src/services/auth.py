import httpx
from urllib.parse import urlencode
import os

GOOGLE_DISCOVERY_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8000/auth/callback"  # FastAPI callback

def get_google_auth_url():
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent"
    }
    return f"{GOOGLE_DISCOVERY_URL}?{urlencode(params)}"

async def exchange_code_for_token(code: str):
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(TOKEN_URL, data=data)
        response.raise_for_status()
        return response.json()

async def get_user_info(access_token: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            USERINFO_URL,
            headers={"Authorization": f"Bearer {access_token}"}
        )
        response.raise_for_status()
        return response.json()
