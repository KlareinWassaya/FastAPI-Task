from fastapi import Depends
from sqlalchemy.orm import Session
from src.repositories.user import UserRepository
from src.services.user import UserService
from src.services.auth import AuthService
from src.common.db.connection import get_db
from src.config.settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_MINUTES

# AuthService is stateless, safe to create once
auth_service = AuthService(SECRET_KEY, ALGORITHM, ACCESS_TOKEN_MINUTES)

def get_user_service(db: Session = Depends(get_db)):
    """Provide UserService with a fresh db session"""
    repo = UserRepository(db)
    return UserService(repo, auth_service)
