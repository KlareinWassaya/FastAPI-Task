from src.repositories.user import UserRepository
from src.common.exceptions.service_custom_exception import ServiceCustomException
from src.services.auth import AuthService
from src.models.user import User
from src.enums.user import UserRole

class UserService:
    def __init__(self, user_repo: UserRepository, auth_service: AuthService):
        self.user_repo = user_repo
        self.auth_service = auth_service

    def get_users(self, role):
        if role != UserRole.ADMIN.value:
            raise ServiceCustomException("permission denied. Permission only allowed for admins")
        return self.user_repo.get_all_users()
    
    # User CRUD
    def create_user(self, username: str, email: str, password: str, role: str = "user"):
        existing_user = self.user_repo.get_by_username(username)
        if existing_user:
            raise ServiceCustomException("User with this username already exists")

        hashed_password = self.auth_service.hash_password(password)
        user = User(username=username, email=email, password_hash=hashed_password, role=role)
        return self.user_repo.create(user)

    # Authentication
    def authenticate_user(self, username: str, password: str):
        user = self.user_repo.get_by_username(username)
        if not user or not self.auth_service.verify_password(password, user.password_hash):
            raise ServiceCustomException("Invalid credentials")
        return user

    def login(self, username: str, password: str):
        user = self.authenticate_user(username, password)
        data = {"sub": str(user.id), "role": user.role}  
        access_token = self.auth_service.create_access_token(data)
        refresh_token = self.auth_service.create_refresh_token(data)
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

    # Refresh
    def refresh(self, refresh_token: str):
        payload = self.auth_service.decode_token(refresh_token)
        if payload.get("scope") != "refresh_token":
            raise ServiceCustomException("Invalid refresh token")
        user_id = payload.get("sub")
        role = payload.get("role")  # carry over the role
        new_access_token = self.auth_service.create_access_token({"sub": user_id, "role": role})
        return {"access_token": new_access_token, "token_type": "bearer"}
