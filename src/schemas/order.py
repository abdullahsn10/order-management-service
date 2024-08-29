from pydantic import BaseModel
from src.schemas.menu_item import (
    MenuItemInPOSTOrderRequestBody,
    MenuItemInGETOrderResponseBody,
)
from src.schemas.customer import CustomerInPOSTOrderRequestBody
from src.models.order import OrderStatus
from datetime import datetime


class OrderPOSTRequestBody(BaseModel):
    """
    pydantic schema for the order in POST request body
    """

    customer_details: CustomerInPOSTOrderRequestBody
    order_items: list[MenuItemInPOSTOrderRequestBody]


class OrderPOSTResponse(BaseModel):
    """
    pydantic schema for the order in POST response body
    """

    id: int
    customer_phone_no: str
    status: OrderStatus


class OrderGETResponse(BaseModel):
    """
    pydantic schema for the order in GET response body
    """

    id: int
    issue_date: datetime
    issuer_id: int
    status: OrderStatus
    customer_id: int
    items: list[MenuItemInGETOrderResponseBody]

    class Config:
        orm_mode = True
        from_attributes = True
