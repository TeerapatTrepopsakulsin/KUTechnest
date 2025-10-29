from typing import Dict, Optional
from dotenv import load_dotenv
from urllib.parse import urlencode
from ..config import settings

import requests
import os

load_dotenv()

BACKEND_URL = settings.BACKEND_URL
FRONTEND_URL = settings.FRONTEND_URL

class GoogleOAuth:

    GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
    GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

    @staticmethod
    def get_authorization_url(state: Optional[str] = None, redirect_uri: Optional[str] = settings.GOOGLE_REDIRECT_URI) -> str:
        params = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": "openid email profile",
            "access_type": "offline",
        }
        if state:
            params["state"] = state

        return f"{GoogleOAuth.GOOGLE_AUTH_URL}?{urlencode(params)}"

    @staticmethod
    def exchange_code_for_token(code: str, redirect_uri: Optional[str] = settings.GOOGLE_REDIRECT_URI) -> Dict:
        data = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        }

        response = requests.post(GoogleOAuth.GOOGLE_TOKEN_URL, 
                                 headers={"Content-Type": "application/x-www-form-urlencoded"}, 
                                 data=data)

        if response.status_code != 200:
            raise Exception(f"Failed to exchange code for token: {response.text}")

        return response.json()

    @staticmethod
    def get_user_info(access_token: str) -> Dict:
        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.get(GoogleOAuth.GOOGLE_USERINFO_URL, headers=headers)

        if response.status_code != 200:
            raise Exception(f"Failed to get user info: {response.text}")

        return response.json()
