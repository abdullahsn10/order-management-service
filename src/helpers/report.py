from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func, asc, desc
from src import schemas, models


def list_customers_orders(
    db: Session,
    from_date: date,
    to_date: date,
    coffee_shop_id: int,
    order_by: str = None,
    sort: str = None,
) -> list[schemas.CustomerOrderReport]:
    """
    This helper function lists all customers along with their total orders and total paid amount
    *Args:
        db (Session): SQLAlchemy Session
        coffee_shop_id (int): coffee shop id to filter customers
        order_by (str): field to order by
        sort (str): sort order
    *Returns:
        list[schemas.CustomerOrderReport]: list of customers along with their total orders or total paid amount
    """
    query = (
        db.query(
            models.Order.customer_id,
            func.coalesce(func.count(func.distinct(models.Order.id)), 0).label(
                "total_orders"
            ),
            func.coalesce(
                func.sum(models.OrderItem.quantity * models.MenuItem.price), 0
            ).label("total_paid"),
        )
        .select_from(models.Order)
        .outerjoin(models.OrderItem, models.Order.id == models.OrderItem.order_id)
        .join(models.MenuItem, models.OrderItem.item_id == models.MenuItem.id)
        .filter(
            models.MenuItem.coffee_shop_id == coffee_shop_id,
            models.Order.issue_date >= from_date,
            models.Order.issue_date <= to_date,
        )
        .group_by(models.Order.customer_id)
    )

    if order_by:
        if sort == "desc":
            query = query.order_by(desc(order_by))
        else:
            query = query.order_by(order_by)  # default asc

    return query.all()


def list_chefs_orders(
    db: Session,
    coffee_shop_id: int,
    from_date: date,
    to_date: date,
    order_by: str = None,
    sort: str = None,
) -> list[schemas.ChefOrderReport]:
    """
    This helper function lists all chefs along with their served orders
    *Args:
        db (Session): SQLAlchemy Session
        coffee_shop_id (int): coffee shop id to filter chefs
        from_date (date): start date to filter orders
        to_date (date): end date to filter orders
        order_by (str): field to order by
        sort (str): sort order
    *Returns:
        list[schemas.ChefOrderReport]: list of chefs along with their served orders
    """
    query = (
        db.query(
            (models.Order.assigner_id).label("chef_id"),
            func.coalesce(func.count(func.distinct(models.Order.id)), 0).label(
                "served_orders"
            ),
        )
        .select_from(models.Order)
        .outerjoin(models.OrderItem, models.Order.id == models.OrderItem.order_id)
        .join(models.MenuItem, models.OrderItem.item_id == models.MenuItem.id)
        .filter(
            models.MenuItem.coffee_shop_id == coffee_shop_id,
            models.Order.issue_date >= from_date,
            models.Order.issue_date <= to_date,
            models.Order.assigner_id != None,
        )
        .group_by(models.Order.assigner_id)
    )

    if order_by:
        if sort == "desc":
            query = query.order_by(desc(order_by))
        else:
            query = query.order_by(order_by)  # default asc

    return query.all()


def list_issuers_orders(
    db: Session,
    coffee_shop_id: int,
    from_date: date,
    to_date: date,
    order_by: str = None,
    sort: str = None,
) -> list[schemas.IssuerOrderReport]:
    """
    This helper function lists all issuers along with their issued orders
    *Args:
        db (Session): SQLAlchemy Session
        coffee_shop_id (int): coffee shop id to filter issuers
        from_date (date): start date to filter orders
        to_date (date): end date to filter orders
        order_by (str): field to order by
        sort (str): sort order
    *Returns:
        list[schemas.IssuerOrderReport]: list of issuers along with their issued orders
    """
    query = (
        db.query(
            (models.Order.issuer_id),
            func.coalesce(func.count(func.distinct(models.Order.id)), 0).label(
                "issued_orders"
            ),
        )
        .select_from(models.Order)
        .outerjoin(models.OrderItem, models.Order.id == models.OrderItem.order_id)
        .join(models.MenuItem, models.OrderItem.item_id == models.MenuItem.id)
        .filter(
            models.MenuItem.coffee_shop_id == coffee_shop_id,
            models.Order.issue_date >= from_date,
            models.Order.issue_date <= to_date,
            models.Order.issuer_id != None,
        )
        .group_by(models.Order.issuer_id)
    )

    if order_by:
        if sort == "desc":
            query = query.order_by(desc(order_by))
        else:
            query = query.order_by(order_by)  # default asc

    return query.all()


def list_orders_income(
    db: Session, coffee_shop_id: int, from_date: date, to_date: date
) -> schemas.OrderIncomeReport:
    """
    This helper function lists total income from orders along with the number of orders
    *Args:
        db (Session): SQLAlchemy Session
        coffee_shop_id (int): coffee shop id to filter orders
        from_date (date): start date to filter orders
        to_date (date): end date to filter orders
    *Returns:
        OrderIncomeReport: total income from orders along with the number of orders
    """
    query = (
        db.query(
            func.count(func.distinct(models.Order.id)).label("total_orders"),
            func.coalesce(
                func.sum(models.OrderItem.quantity * models.MenuItem.price), 0
            ).label("total_income"),
        )
        .select_from(models.Order)
        .outerjoin(models.OrderItem, models.Order.id == models.OrderItem.order_id)
        .outerjoin(models.MenuItem, models.MenuItem.id == models.OrderItem.item_id)
        .filter(
            models.MenuItem.coffee_shop_id == coffee_shop_id,
            models.Order.issue_date >= from_date,
            models.Order.issue_date <= to_date,
        )
    )

    result = query.first()
    return schemas.OrderIncomeReport(
        total_income=result.total_income,
        total_orders=result.total_orders,
    )


def list_top_selling_items(
    db: Session, coffee_shop_id: int, from_date: date, to_date: date, sort: str = None
) -> schemas.TopSellingItemsReport:
    """
    This helper function lists top selling items along with their total quantity
    *Args:
        db (Session): SQLAlchemy Session
        coffee_shop_id (int): coffee shop id to filter items
        from_date (date): start date to filter orders
        to_date (date): end date to filter orders
        sort (str): sort order
    *Returns:
        TopSellingItemsReport: top selling items along with their total quantity
    """
    query = (
        db.query(
            models.MenuItem.id,
            func.array_agg(models.MenuItem.name)[1].label("item_name"),
            func.coalesce(func.sum(models.OrderItem.quantity), 0).label(
                "selling_times"
            ),
        )
        .select_from(models.MenuItem)
        .join(models.OrderItem, models.MenuItem.id == models.OrderItem.item_id)
        .join(models.Order, models.OrderItem.order_id == models.Order.id)
        .filter(
            models.MenuItem.coffee_shop_id == coffee_shop_id,
            models.Order.issue_date >= from_date,
            models.Order.issue_date <= to_date,
        )
        .group_by(models.MenuItem.id)
    )

    if sort == "desc":
        query = query.order_by(desc("selling_times"))
    else:
        query = query.order_by("selling_times")  # default asc

    result = query.all()
    return schemas.TopSellingItemsReport(top_selling_items=result)
