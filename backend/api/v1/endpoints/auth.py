from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import Optional
from ....core.database import get_db
from ....schemas.user import TokenResponse, GoogleLoginURLResponse, UserResponse, UserRoleResponse
from ....schemas.company import CompanyResponse
from ....schemas.student import StudentResponse
from ....schemas.registration import StudentRegistrationRequest, CompanyRegistrationRequest
from ....crud import user as crud_user, student as crud_student, company as crud_company
from ....utils.google_oauth import GoogleOAuth
from ....utils.auth import create_access_token, get_current_user, security
from ....models.user import User
from ....config import settings
from fastapi.security import HTTPAuthorizationCredentials

router = APIRouter()


@router.get("/debug-settings")
async def debug_settings():
    """Debug endpoint to verify settings"""
    return {
        "secret_key_prefix": settings.SECRET_KEY[:5],
        "algorithm": settings.ALGORITHM,
        "token_expire": settings.ACCESS_TOKEN_EXPIRE_MINUTES
    }


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
                    profile_picture=picture,
                    role=user_role  # Use the role passed from the frontend
                )

        from ....crud import student as crud_student
        from ....crud import company as crud_company

        # Check if user has completed registration
        student = crud_student.get_student_by_user_id(db, user.id)
        company = crud_company.get_company_by_user_id(db, user.id)

        if student:
            user_role = "student"
            user_status = "active"
        elif company:
            user_role = "company"
            user_status = "active"
        else:
            user_role = user.role if user.role else "user"
            user_status = user.status if user.status else "pending"

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


@router.post("/register/student", response_model=TokenResponse)
async def register_student(
    student_data: StudentRegistrationRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Register a new student after Google OAuth authentication.
    
    This endpoint creates a new student profile for an authenticated user.
    It requires a valid JWT token from the Google OAuth process.
    """
    current_user = get_current_user(credentials, db)  # Get user with debug logging
    try:
        from ....crud import registration as crud_registration
        
        # Create new student profile
        student = crud_registration.register_student(
            db=db,
            user_id=current_user.id,
            student_data=student_data
        )
        
        # Update current_user with role and status
        current_user.role = "student"
        current_user.status = "active"
        db.commit()

        user_dict = UserResponse.from_orm(current_user).model_dump()
        user_dict["role"] = current_user.role
        user_dict["status"] = current_user.status

        # Generate new token with updated claims
        jwt_token = create_access_token(data={"sub": current_user.id})

        return {
            "access_token": jwt_token,
            "token_type": "bearer",
            "user": user_dict
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to register student: {str(e)}"
        )

@router.post("/register/company", response_model=TokenResponse)
async def register_company(
    company_data: CompanyRegistrationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Register a new company after Google OAuth authentication.
    
    This endpoint creates a new company profile for an authenticated user.
    It requires a valid JWT token from the Google OAuth process.
    """
    try:
        from ....crud import registration as crud_registration
        
        # Create new company profile
        company = crud_registration.register_company(
            db=db,
            user_id=current_user.id,
            company_data=company_data
        )
        
        # Update current_user with role and status
        current_user.role = "company"
        current_user.status = "active"
        db.commit()

        user_dict = UserResponse.from_orm(current_user).model_dump()
        user_dict["role"] = current_user.role
        user_dict["status"] = current_user.status

        # Generate new token with updated claims
        jwt_token = create_access_token(data={"sub": current_user.id})

        return {
            "access_token": jwt_token,
            "token_type": "bearer",
            "user": user_dict
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to register company: {str(e)}"
        )

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
    user = crud_user.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get profile data based on role
    data = None
    if user.role == "company":
        company = crud_company.get_company_by_user_id(db, user_id)
        if company:
            data = CompanyResponse.from_orm(company)
    elif user.role == "student":
        student = crud_student.get_student_by_user_id(db, user_id)
        if student:
            data = StudentResponse.from_orm(student)

    # If user has role but no profile, they're still in registration process
    if not data and user.role:
        status = user.status
        role = user.role
    else:
        # User must have a role and profile to be active
        role = user.role if user.role else "user"
        status = user.status if user.status else "pending"

    roleData = {"role": role, "status": status, "data": data}
    return UserRoleResponse(**roleData)
