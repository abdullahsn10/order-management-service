from enum import Enum


class UserRole(Enum):
    """
    Enum class to represent the role of a user.
    'cashier', 'chef', 'order_receiver', 'admin'
    """

    ADMIN = "ADMIN"
    CASHIER = "CASHIER"
    CHEF = "CHEF"
    ORDER_RECEIVER = "ORDER_RECEIVER"
