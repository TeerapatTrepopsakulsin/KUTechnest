from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import Optional, Literal
from dotenv import load_dotenv
from ....core.database import get_db
from ....schemas.user import TokenResponse, GoogleRegisterURLResponse, GoogleLoginURLResponse, UserResponse, UserRoleResponse
from ....schemas.company import CompanyCreate, CompanyResponse
from ....schemas.student import StudentCreate, StudentResponse
from ....crud import user as crud_user, student as crud_student, company as crud_company
from ....utils.google_oauth import GoogleOAuth
from ....utils.auth import create_access_token, get_current_user
from ....models.user import User
from ....config import settings

import secrets
import os

router = APIRouter()

load_dotenv()

BACKEND_URL = settings.BACKEND_URL
FRONTEND_URL = settings.FRONTEND_URL


@router.get("/google/register/{role}", response_model=GoogleLoginURLResponse)
async def google_register(request: Request, role: Literal["student", "company"]):
    """
    Returns the Google OAuth2 registration URL for user authentication.

    This endpoint generates and returns the authorization URL that redirects users
    to Google's consent screen where they can grant permission to access their profile.
    """
    try:
        if role not in ["student", "company"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid role specified"
            )

        auth_url = GoogleOAuth.get_authorization_url(state=role, redirect_uri=FRONTEND_URL+"/register/"+role)
        return GoogleRegisterURLResponse(url=auth_url)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate login URL: {str(e)}"
        )
    

@router.get("/google/callback/register", response_model=TokenResponse)
async def google_register_callback(
    request: Request,
    code: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    error: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Handles the OAuth2 callback from Google after user consent for registration.

    This endpoint receives the authorization code from Google, exchanges it for
    access tokens, retrieves the user's profile information, and creates a new user
    along with their associated student or company profile. Returns a JWT access token
    for subsequent authenticated requests.

    Args:
        code: Authorization code from Google OAuth flow
        error: Error message if authentication failed
        db: Database session

    Returns:
        TokenResponse with access token and user information

    Error:
        HTTP 502 if any step in the Google Overhead Fails
        HTTP 409 if user already registered
        HTTP 401 if session data not found or expired
        HTTP 400 if invalid role specified in session data
    """
    if error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Google authentication error: {error}"
        )

    if not code or not state:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Authorization code or state not provided"
        )
    
    try:
        token_data = GoogleOAuth.exchange_code_for_token(code, redirect_uri=BACKEND_URL+"/api/v1/auth/google/register/callback")
        access_token = token_data.get("access_token")

        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
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
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Failed to retrieve user information from Google"
            )

        user = crud_user.get_user_by_google_id(db, google_id)
        if user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already registered"
            )

        session_data = request.session.pop(state, None)
        if not session_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session data not found or expired"
            )

        role = session_data.pop("role")

        user = crud_user.create_user(
            db=db,
            email=email,
            first_name=given_name,
            last_name=family_name,
            google_id=google_id,
            profile_picture=picture
        )

        return RedirectResponse(FRONTEND_URL+'register/'+role)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Authentication failed: {str(e)}"
        )

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
            # TODO: Tempory disable error while debugging
            # --------------------------
            else:
                pass
            #     raise HTTPException(
            #     status_code=status.HTTP_401_UNAUTHORIZED,
            #     detail="Have not authorized as student"
            # )
            # --------------------------
        else:
            company = crud_company.get_company_by_user_id(db, user.id)
            if company:
                user_status = "approved"
            # TODO: Tempory disable error while debugging
            # --------------------------
            else:
                pass
            #     raise HTTPException(
            #     status_code=status.HTTP_401_UNAUTHORIZED,
            #     detail="Have not authorized as company"
            # )
            # --------------------------

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


@router.get("/user/{user_id}/role", response_model=UserRoleResponse)
async def get_user_info(user_id: int, db: Session = Depends(get_db)):
    """
    Returns a user's role information by user ID.

    This endpoint retrieves the user profile for the specified user ID.
    It is useful for fetching public role based user information.

    Args:
        user_id: ID of the user to retrieve
        db: Database session
    Returns:
        UserRoleResponse with the specified user's role information
    """
    company = crud_company.get_company_by_user_id(db, user_id)
    student = crud_student.get_student_by_user_id(db, user_id)
    if company:
        role = "company"
        status = "approved"
        data = CompanyResponse.from_orm(company)
    elif student:
        role = "student"
        status = "approved"
        data = StudentResponse.from_orm(student)
    else:
        raise HTTPException(status_code=404, detail="User not found")

    roleData = {"role": role, "status": status, "data": data}
    userRole = UserRoleResponse.model_validate(roleData)
    return UserRoleResponse.from_orm(userRole)
