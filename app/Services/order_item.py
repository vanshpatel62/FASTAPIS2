from sqlalchemy.orm import Session
from app.Models import OrderItem
from fastapi import HTTPException

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_order_items(db: Session):
    try:
        logger.info("Fetching all order items...")

        order_items = db.query(OrderItem).all()

        logger.info(
            "Successfully fetched %d order item(s)",
            len(order_items)
        )

        return order_items

    except Exception:
        db.rollback()   # Optional for SELECT, but safe
        logger.error("Failed to fetch order items")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch order items"
        )