from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import Optional
from ....core.database import get_db
from ....schemas.user import TokenResponse, GoogleLoginURLResponse, UserResponse
from ....crud import user as crud_user
from ....utils.google_oauth import GoogleOAuth
from ....utils.auth import create_access_token, get_current_user
from ....models.user import User

router = APIRouter()


@router.get("/google/login", response_model=GoogleLoginURLResponse)
async def google_login(role: str = Query("student")):
    """
    Returns the Google OAuth2 login URL for user authentication.

    This endpoint generates and returns the authorization URL that redirects users
    to Google's consent screen where they can grant permission to access their profile.
    """
    try:
        auth_url = GoogleOAuth.get_authorization_url(state=role)
        return GoogleLoginURLResponse(url=auth_url)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate login URL: {str(e)}"
        )


@router.get("/google/callback", response_model=TokenResponse)
async def google_callback(
    code: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    role: Optional[str] = Query(None),
    error: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Handles the OAuth2 callback from Google after user consent.

    This endpoint receives the authorization code from Google, exchanges it for
    access tokens, retrieves the user's profile information, and either creates
    a new user or updates an existing one. Returns a JWT access token for subsequent
    authenticated requests.

    Args:
        code: Authorization code from Google OAuth flow
        error: Error message if authentication failed
        db: Database session

    Returns:
        TokenResponse with access token and user information
    """
    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Google authentication error: {error}"
        )

    if not code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authorization code not provided"
        )

    try:
        token_data = GoogleOAuth.exchange_code_for_token(code)
        access_token = token_data.get("access_token")

        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to obtain access token"
            )

        user_info = GoogleOAuth.get_user_info(access_token)

        email = user_info.get("email")
        google_id = user_info.get("id")
        given_name = user_info.get("given_name", "")
        family_name = user_info.get("family_name", "")
        picture = user_info.get("picture")

        if not email or not google_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to retrieve user information from Google"
            )

        user = crud_user.get_user_by_google_id(db, google_id)
        user_role = state or role or "student"

        if not user:
            user = crud_user.get_user_by_email(db, email)
            if user:
                user = crud_user.update_user_oauth_info(db, user, google_id, picture)
            else:
                user = crud_user.create_user(
                    db=db,
                    email=email,
                    first_name=given_name,
                    last_name=family_name,
                    google_id=google_id,
                    profile_picture=picture
                )

        from ....crud import student as crud_student
        from ....crud import company as crud_company

        user_status = "pending"
        if user_role == "student":
            student = crud_student.get_student_by_user_id(db, user.id)
            if student:
                user_status = "approved"
        else:
            company = crud_company.get_company_by_user_id(db, user.id)
            if company:
                user_status = "approved"

        jwt_token = create_access_token(data={"sub": user.id})

        user_response = UserResponse.from_orm(user)
        user_dict = user_response.model_dump()
        user_dict["role"] = user_role
        user_dict["status"] = user_status

        return {
            "access_token": jwt_token,
            "token_type": "bearer",
            "user": user_dict
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Authentication failed: {str(e)}"
        )


@router.get("/user/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Returns the authenticated user's profile information.

    This is a protected endpoint that requires a valid JWT token in the
    Authorization header. It returns the complete user profile including
    email, name, and profile picture.

    Args:
        current_user: Authenticated user from JWT token (injected by dependency)

    Returns:
        UserResponse with the current user's information
    """
    return UserResponse.from_orm(current_user)
