from pydantic import BaseModel


class CustomerOrderReport(BaseModel):
    """
    pydantic model for customer order report
    """

    customer_id: int
    total_orders: int
    total_paid: float

    class Config:
        orm_mode = True
        from_attributes = True
