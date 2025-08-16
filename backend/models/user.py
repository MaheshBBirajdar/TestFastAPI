from pydantic import BaseModel
from typing import Optional
from enum import Enum

# Enum for roles
class RoleStatus(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"

class UserBase(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    role: RoleStatus = RoleStatus.USER
    is_active: Optional[bool] = True

class UserCreate(UserBase):
    password: str   # plain password (will be hashed before saving)

class UserUpdate(BaseModel):
    user_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[RoleStatus] = None
    is_active: Optional[bool] = None

class UserGet(BaseModel):
    user_id: int

    class Config:
        from_attributes = True  # Pydantic v2 (use orm_mode=True in v1)

class UserOut(BaseModel):
    user_id: int

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True   # Pydantic v2 (use orm_mode=True in v1)
