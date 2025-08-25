from fastapi import Depends, Request, HTTPException, status
from src.services.auth import AuthService
from src.services.user import UserService
from src.dependencies.user import get_user_service
from src.config.settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_MINUTES

# AuthService is stateless; safe to create once
auth_service = AuthService(secret_key=SECRET_KEY, algorithm=ALGORITHM, access_token_expires_minutes=ACCESS_TOKEN_MINUTES)


def get_current_user(
    request: Request,
    user_service: UserService = Depends(get_user_service)
):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing or invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = auth_header.split(" ")[1]
    payload = auth_service.decode_token(token)
    
    user_id = payload.get("sub")
    role = payload.get("role")  # <-- get role from token
    
    user = user_service.user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Attach role to user object (or return a dict if using plain models)
    user.role = role  
    return user
