import datetime
from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from fastapi import status
from src import schemas, models
from src.exceptions import OrderServiceException
from src.helpers import customer, menu_item, user
from src.models.order import OrderStatus
from collections import defaultdict
from src.definition import ROLE_STATUS_MAPPING
from src.security.roles import UserRole
from src.utils.rabbitmq import RabbitMQClient
from src.data.notification import Notification
from src.settings.settings import (
    RABBITMQ_HOST,
    RABBITMQ_USER,
    RABBITMQ_PASSWORD,
    ORDER_NOTIFICATION_QUEUE,
    ORDERS_CACHE_KEY,
    ORDERS_CACHE_EXPIRATION,
)
from src.utils.redis_caching import CacheManager
from src.utils.json_encoder import DateTimeEncoder
import json


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


def _create_order_notification(
    order_id: int, issuer_id: int, customer_id: int, coffee_shop_id: int
):
    """
    This helper function used to create a new order notification
    *Args:
        order_id (int): the order id
        issuer_id (int): the issuer id of the order
        customer_id (int): the customer id of the order
        coffee_shop_id (int): the coffee shop id of the order
    *Returns:
        None
    """
    message = f"Order with id={order_id} has been created successfully by issuer {issuer_id} for customer {customer_id}"
    notification = Notification(
        order_id=order_id,
        issuer_id=issuer_id,
        customer_id=customer_id,
        coffee_shop_id=coffee_shop_id,
        message=message,
        created_at=datetime.now(),
    )
    notification = json.dumps(notification.to_dict())
    (
        RabbitMQClient(
            host=RABBITMQ_HOST,
            username=RABBITMQ_USER,
            password=RABBITMQ_PASSWORD,
        ).publish_message(queue_name=ORDER_NOTIFICATION_QUEUE, message=notification)
    )


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

    # Create order notification
    _create_order_notification(
        order_id=created_order.id,
        issuer_id=issuer_id,
        customer_id=created_customer_instance.id,
        coffee_shop_id=coffee_shop_id,
    )

    return schemas.OrderPOSTResponse(
        id=created_order.id,
        customer_phone_no=created_customer_instance.phone_no,
        status=created_order.status,
    )


def find_order(order_id: int, db: Session, coffee_shop_id: int = None) -> models.Order:
    """
    This helper function used to find a specific order
    *Args:
        order_id (int): the order id needed to be found
        db (Session): a database session
        coffee_shop_id (int): id of the coffee shop to find the order for
    *Returns:
        the found order if it exists, raise OrderServiceException otherwise
    """
    query = (
        db.query(models.Order)
        .options(joinedload(models.Order.items))
        .filter(models.Order.id == order_id)
    )
    if coffee_shop_id:
        query = (
            query.join(models.OrderItem)
            .join(models.MenuItem)
            .filter(
                models.MenuItem.coffee_shop_id == coffee_shop_id,
                models.OrderItem.item_id == models.MenuItem.id,
            )
        )
    found_order = query.first()
    if not found_order:
        raise OrderServiceException(
            message=f"This order with id ={order_id} does not exist",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return found_order


def _find_all_orders(
    db: Session,
    coffee_shop_id: int,
    size: int,
    page: int,
    status: list[OrderStatus] = None,
) -> tuple[list[models.Order], int]:
    """
    This helper function used to find all orders in the coffee_shop with specific status
    and apply a pagination on the resulted orders
    *Args:
        db (Session): a database session
        coffee_shop_id (int): id of the coffee shop to find the orders for
        status (str): the status of the orders to find
        size (int): the maximum number of orders to return
        page (int): the page number, needed to calculate the offset to skip
    *Returns:
        a list of all orders in the coffee_shop within specific page and limit,
        in addition to the total count of orders in the system
    """

    query = db.query(models.Order).options(joinedload(models.Order.items))
    if coffee_shop_id:
        query = (
            query.join(models.OrderItem)
            .join(models.MenuItem)
            .filter(
                models.MenuItem.coffee_shop_id == coffee_shop_id,
                models.OrderItem.item_id == models.MenuItem.id,
            )
        )
    if status:
        query = query.filter(models.Order.status.in_(status))

    # total count of orders
    total_count: int = query.distinct(models.Order.id).count()

    # apply pagination
    offset = (page - 1) * size
    orders = query.offset(offset).limit(size).all()

    return orders, total_count


def _get_cached_orders(
    coffee_shop_id: int, page: int, size: int, status: list[OrderStatus]
) -> dict:
    """
    This helper function used to get all orders from the cache, All args are used to
    create a unique key for the cache
    *Args:
        coffee_shop_id (int): id of the coffee shop to find the orders for
        status (str): the status of the orders needed to be retrieved
        page (int): the page number, needed to calculate the offset to skip
        size (int): the maximum limit of orders to return in the page
    *Returns:
        a JSON / dictionary contains the cached orders if exists, None otherwise
    """
    cache_manager = CacheManager()
    cache_key = ORDERS_CACHE_KEY.format(
        coffee_shop_id=coffee_shop_id, status=status, page=page, size=size
    )
    try:
        cached_response = cache_manager.get_cache(key=cache_key)
        if cached_response:
            print(f"Cache hit for key {cache_key}")  # Will be replaced with logger
            return json.loads(cached_response)
        else:
            print(f"Cache miss for key {cache_key}")  # Will be replaced with logger
    except Exception as e:
        print(f"Error while reading from cache: {e}")  # Will be replaced with logger
    return None


def _cache_orders_response(
    coffee_shop_id: int,
    status: list[OrderStatus],
    page: int,
    size: int,
    response: schemas.PaginatedOrderResponse,
) -> None:
    """
    This helper function used to cache the orders response
    *Args:
        coffee_shop_id (int): id of the coffee shop to find the orders for
        status (str): the status of the orders needed to be retrieved
        page (int): the page number, needed to calculate the offset to skip
        size (int): the maximum limit of orders to return in the page
        response (schemas.PaginatedOrderResponse): the response to be cached
    *Returns:
        None
    """
    cache_manager = CacheManager()
    cache_key = ORDERS_CACHE_KEY.format(
        coffee_shop_id=coffee_shop_id, status=status, page=page, size=size
    )
    try:
        cache_manager.set_cache(
            key=cache_key,
            value=json.dumps(response.dict(), cls=DateTimeEncoder),
            expire=ORDERS_CACHE_EXPIRATION,
        )
    except Exception as e:
        print(f"Error while writing to cache: {e}")  # Will be replaced with logger


def get_all_orders(
    status: list[OrderStatus], db: Session, coffee_shop_id: int, page: int, size: int
) -> schemas.PaginatedOrderResponse:
    """
    This helper function used to get all orders along with their details (paginated)
    *Args:
        status (str): the status of the orders needed to be retrieved
        db (Session): a database session
        coffee_shop_id (int): id of the coffee shop to find the orders for
        page (int): the page number, needed to calculate the offset to skip
        size (int): the maximum limit of orders to return in the page
    *Returns:
        PaginatedOrderResponse instance contains the orders details
    """

    cached_response = _get_cached_orders(
        coffee_shop_id=coffee_shop_id, status=status, page=page, size=size
    )

    if cached_response:
        return schemas.PaginatedOrderResponse(**cached_response)

    # if cache miss or read failed, fetch from database
    all_orders, total_count = _find_all_orders(
        db=db, status=status, coffee_shop_id=coffee_shop_id, size=size, page=page
    )

    response = schemas.PaginatedOrderResponse(
        total_count=total_count,
        page=page,
        page_size=size,
        orders=all_orders,
    )

    # Cache the response
    _cache_orders_response(
        coffee_shop_id=coffee_shop_id,
        status=status,
        page=page,
        size=size,
        response=response,
    )

    return response


def _validate_status_change(new_status: str, user_role: str) -> None:
    """
    This helper function used to validate the change in the status of the order
    *Args:
        new_status (OrderStatus): the new status of the order
        user_role (UserRole): the role of the user who tries to change the statu
    *Returns:
        raise an OrderServiceException in case of violation
    """

    if new_status not in ROLE_STATUS_MAPPING[user_role]:
        raise OrderServiceException(
            message="Unacceptable change of the status",
            status_code=status.HTTP_400_BAD_REQUEST,
        )


def update_order_status(
    request: schemas.OrderStatusPATCHRequestBody,
    order_id: int,
    user_role: str,
    coffee_shop_id: int,
    db: Session,
) -> None:
    """
    This helper function used to update an order status, it applies conditions on
    the new status of the order along with the role of the user who
    tries to change this status
    *Args:
        request (schemas.OrderStatusPATCHRequestBody): the request body which contains the new status
        order_id (int): the order id needed to be changed
        coffee_shop_id (int): id of the coffee shop to find the order for
        user_role (UserRole): the role of the user needs to update the order's status
        db (Session): a database session
    *Returns:
        None in case of success, raise OrderServiceException in case of any failure
    """
    found_order = find_order(order_id=order_id, coffee_shop_id=coffee_shop_id, db=db)
    _validate_status_change(new_status=request.status.value, user_role=user_role)
    found_order.status = request.status
    db.commit()


def assign_order(
    order_id: int,
    chef_id: int,
    coffee_shop_id: int,
    db: Session,
    auth_token: str = None,
) -> None:
    """
    This helper function used to assign a specific order to a specific chef
    *Args:
        order_id (int): the order id needed to be assigned
        chef_id (int): the chef id needed to be assigned to
        coffee_shop_id(int): the coffee shop id of the user and the order
        db (Session): a database session
    *Returns:
        None in case of success, raise ShopsAppException in case of any failure
    """
    found_order = find_order(order_id=order_id, db=db, coffee_shop_id=coffee_shop_id)
    found_user = user._find_user(user_id=chef_id, auth_token=auth_token)
    if found_user.role != UserRole.CHEF:
        raise OrderServiceException(
            message="The assigner must be a chef",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    found_order.assigner_id = found_user.id
    db.commit()
