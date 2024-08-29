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


class ChefOrderReport(BaseModel):
    """
    pydantic model for chef order report
    """

    chef_id: int
    served_orders: int

    class Config:
        orm_mode = True
        from_attributes = True


class IssuerOrderReport(BaseModel):
    """
    pydantic model for issuer order report
    """

    issuer_id: int
    issued_orders: int

    class Config:
        orm_mode = True
        from_attributes = True
