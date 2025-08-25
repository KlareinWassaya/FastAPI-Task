from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str   # plain password for registration
    role: Optional[str] = "user"

class UserRead(UserBase):
    id: int
    is_active: bool
    role: str

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str

class RefreshRequest(BaseModel):
    refresh_token: str
