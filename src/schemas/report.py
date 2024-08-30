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


class OrderIncomeReport(BaseModel):
    """
    pydantic model for order income
    """

    total_orders: int
    total_income: float

    class Config:
        orm_mode = True
        from_attributes = True


class SoldItemResponse(BaseModel):
    """
    pydantic model for top selling items report
    """

    id: int
    item_name: str
    selling_times: int

    class Config:
        orm_mode = True
        from_attributes = True


class TopSellingItemsReport(BaseModel):
    """
    pydantic model for top selling items report
    """

    top_selling_items: list[SoldItemResponse]

    class Config:
        orm_mode = True
        from_attributes = True
