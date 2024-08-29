from pydantic import BaseModel
from src.security.roles import UserRole


class UserResponse(BaseModel):
    """
    Pydantic schema for User response
    """

    id: int
    first_name: str
    last_name: str
    email: str
    phone_no: str
    role: UserRole
    branch_id: int

    class Config:
        orm_mode = True
        from_attributes = True
