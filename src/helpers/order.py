import datetime
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload
from fastapi import status
from src import schemas, models
from src.exceptions import OrderServiceException
from src.helpers import customer, menu_item
from src.models.order import OrderStatus
from collections import defaultdict


def _validate_order_items(
    items_list: list[schemas.MenuItemInPOSTOrderRequestBody],
    coffee_shop_id: int,
    db: Session,
):
    """
    This helper function used to validate all items in an order that they are exist and the
    order is not empty
    *Args:
        items_list (list[schemas.MenuItemInPOSTOrderRequestBody]): a list of order items
        db (Session): a database session
    *Returns:
        raise an exception if any item is not found
    """
    if not items_list:
        raise OrderServiceException(
            status_code=status.HTTP_400_BAD_REQUEST, message="Order items are empty"
        )
    for item in items_list:
        menu_item._find_menu_item(
            db=db, menu_item_id=item.id, coffee_shop_id=coffee_shop_id
        )


def _create_order(
    customer_id: int,
    issuer_id: int,
    db: Session,
    order_items: list[schemas.MenuItemInPOSTOrderRequestBody],
) -> models.Order:
    """
    This helper function used to create a new order instance
    *Args:
        customer_id (int): the customer id
        issuer_id (int): the issuer id of the order
        db (Session): a database session
    *Returns:
        the created order instance
    """

    created_order = models.Order(
        customer_id=customer_id,
        issuer_id=issuer_id,
        status=OrderStatus.PENDING,
        issue_date=datetime.now(),
    )
    db.add(created_order)
    db.commit()
    db.refresh(created_order)

    # sum quantities of items with the same id
    item_quantities = defaultdict(int)
    for item in order_items:
        item_quantities[item.id] += item.quantity

    # Create order details after aggregation
    for item_id, total_quantity in item_quantities.items():
        db.add(
            models.OrderItem(
                order_id=created_order.id,
                item_id=item_id,
                quantity=total_quantity,  # Use aggregated quantity
            )
        )
    db.commit()  # commit after adding all items

    return created_order


def place_an_order(
    request: schemas.OrderPOSTRequestBody,
    coffee_shop_id: int,
    issuer_id: int,
    auth_token: str,
    db: Session,
) -> schemas.OrderPOSTResponse:
    """
    This helper function used to place an order
    *Args:
        request (schemas.OrderPOSTRequestBody): details of the order
        coffee_shop_id (int): id of the coffee shop to create the order for
        issuer_id (int): id of the user (chef or order_receiver) who created the order
        db (Session): database session
        auth_token (str): the token of the user who created the order (for calling external services)
    *Returns:
        the created order details (schemas.OrderPOSTResponseBody)
    """

    customer_details: schemas.CustomerInPOSTOrderRequestBody = request.customer_details
    order_items: list[schemas.MenuItemInPOSTOrderRequestBody] = request.order_items

    _validate_order_items(items_list=order_items, db=db, coffee_shop_id=coffee_shop_id)

    # Create customer
    created_customer_instance = customer._get_or_create_customer(
        request=customer_details,
        auth_token=auth_token,
    )

    # Create order and its items
    created_order = _create_order(
        customer_id=created_customer_instance.id,
        issuer_id=issuer_id,
        db=db,
        order_items=order_items,
    )

    return schemas.OrderPOSTResponse(
        id=created_order.id,
        customer_phone_no=created_customer_instance.phone_no,
        status=created_order.status,
    )
