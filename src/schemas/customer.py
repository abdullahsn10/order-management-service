from pydantic import BaseModel
from datetime import datetime


class CustomerInPOSTOrderRequestBody(BaseModel):
    """
    pydantic schema for the customer details in the order POST request body
    """

    name: str
    phone_no: str

    class Config:
        orm_mode = True
        from_attributes = True


class CustomerFullInfo(BaseModel):
    """
    pydantic schema for the customer full info
    """

    id: int
    name: str
    phone_no: str
    coffee_shop_id: int
    created: datetime

    class Config:
        orm_mode = True
        from_attributes = True
