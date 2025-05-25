from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from firebase_admin import auth as firebase_auth, credentials, initialize_app, get_app
from firebase_admin.exceptions import FirebaseError
from src.services.auth import get_google_auth_url, exchange_code_for_token, get_user_info
from src.utils.jwt_handler import create_jwt
from src.database.connection import get_db
import logging

logger = logging.getLogger(__name__)
router = APIRouter(tags=["auth"])

# Firebase init
try:
    cred = credentials.Certificate("promptstudio-76ab4-ba16da252818.json")
    try:
        get_app()
    except ValueError:
        initialize_app(cred)
except Exception as e:
    logger.error(f"Firebase init error: {e}")

@router.get("/auth/google")
async def login_with_google():
    auth_url = get_google_auth_url()
    return RedirectResponse(auth_url)

@router.get("/auth/callback")
async def google_callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Missing authorization code")

    try:
        token_response = await exchange_code_for_token(code)
        access_token = token_response.get("access_token")
        user_info = await get_user_info(access_token)

        email = user_info.get("email")
        name = user_info.get("name")
        if not email:
            raise HTTPException(status_code=400, detail="Email not found in user info")

        try:
            firebase_auth.get_user_by_email(email)
        except FirebaseError:
            firebase_auth.create_user(email=email)

        db = get_db()
        users_collection = db['users']
        existing_user = users_collection.find_one({"email": email})
        if not existing_user:
            users_collection.insert_one({
                "email": email,
                "name": name,
                "role" : "user",
                "auth_provider": "google",
            })
        jwt_token = create_jwt(email, name)
        redirect_url = f"http://localhost:8501/?token={jwt_token}"
        return RedirectResponse(redirect_url)

    except Exception as e:
        logger.error(f"Google auth callback error: {e}")
        raise HTTPException(status_code=500, detail="OAuth callback failed")
