from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from src.common.exceptions.service_custom_exception import ServiceCustomException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, secret_key: str, algorithm: str, access_token_expires_minutes: int):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expires_minutes = access_token_expires_minutes

    # Hash passwords
    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    # Token creation
    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expires_minutes)
        to_encode.update({
            "exp": expire,
            "scope": "access_token",
            "role": data.get("role")  
        })
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def create_refresh_token(self, data: dict, days: int = 7):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=days)
        to_encode.update({"exp": expire, "scope": "refresh_token"})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    # Token decoding
    def decode_token(self, token: str):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            raise ServiceCustomException("Invalid token")
