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
