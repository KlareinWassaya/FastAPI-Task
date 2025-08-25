from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.services.user import UserService
from src.schemas.user import TokenResponse, RefreshRequest, UserCreate, UserRead
from src.dependencies.user import get_user_service
from src.dependencies.auth import get_current_user


router = APIRouter(prefix="/users", tags=["user"])


@router.post("/register", response_model=dict)
def register(data: UserCreate, auth_service: UserService = Depends(get_user_service)):
    user = auth_service.create_user(username=data.username, email=data.email, password=data.password, role=data.role)
    return {"message": "User created successfully", "user_id": user.id}
    

@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(get_user_service)
):
    return user_service.login(form_data.username, form_data.password)

@router.post("/refresh", response_model=TokenResponse)
def refresh(data: RefreshRequest, auth_service: UserService = Depends(get_user_service)):
    return auth_service.refresh(data.refresh_token)

@router.get("/", response_model=list[UserRead])
def get_users(
    user_service: UserService = Depends(get_user_service),
    current_user = Depends(get_current_user)
):
    return user_service.get_users(role=current_user.role)