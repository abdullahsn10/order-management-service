from typing import Optional, List
from fastapi import APIRouter, HTTPException, Depends, Response, status, Query
from src import schemas
from src.security.roles import UserRole
from sqlalchemy.orm import Session
from src.settings.database import get_db
from src.exceptions.exception import OrderServiceException
from src.security.oauth2 import require_role
from src.helpers import order
from src.models.order import OrderStatus

router = APIRouter(
    tags=["Orders"],
    prefix="/orders",
)


@router.post("/", response_model=schemas.OrderPOSTResponse)
def place_an_order_endpoint(
    request: schemas.OrderPOSTRequestBody,
    response: Response,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(
        require_role([UserRole.ORDER_RECEIVER, UserRole.CASHIER, UserRole.ADMIN])
    ),
):
    """
    POST endpoint to place an order
    """
    try:
        response.status_code = status.HTTP_201_CREATED
        return order.place_an_order(
            request=request,
            coffee_shop_id=current_user.coffee_shop_id,
            issuer_id=current_user.id,
            db=db,
            auth_token=current_user.token_value,
        )
    except OrderServiceException as se:
        raise HTTPException(status_code=se.status_code, detail=se.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
