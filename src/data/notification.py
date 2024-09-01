from dataclasses import dataclass
from datetime import datetime


@dataclass
class Notification:
    """
    Notification dataclass
    """

    order_id: int
    issuer_id: int
    customer_id: int
    message: str
    created_at: datetime

    def to_dict(self):
        """convert Notification instance to a dictionary with ISO formatted datetime."""
        return {
            "order_id": self.order_id,
            "issuer_id": self.issuer_id,
            "customer_id": self.customer_id,
            "message": self.message,
            "created_at": self.created_at.isoformat(),
        }
