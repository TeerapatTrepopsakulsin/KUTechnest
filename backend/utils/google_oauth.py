import requests
from typing import Dict, Optional
from ..config import settings


class GoogleOAuth:

    GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
    GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

    @staticmethod
    def get_authorization_url(state: Optional[str] = None) -> str:
        params = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "response_type": "code",
            "scope": "openid email profile",
            "access_type": "offline",
        }
        if state:
            params["state"] = state

        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"{GoogleOAuth.GOOGLE_AUTH_URL}?{query_string}"

    @staticmethod
    def exchange_code_for_token(code: str) -> Dict:
        data = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }

        response = requests.post(GoogleOAuth.GOOGLE_TOKEN_URL, data=data)

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
