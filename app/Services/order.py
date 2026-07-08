from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.Models import Order

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



# def get_order(db: Session):
#     result = db.execute(text("select * from orders order by order_id"))
#     return result.fetchall()


# def search_order_by_order_id(ord_id: int, db: Session):
#     order_details = db.query(Order).filter_by(order_id=ord_id).all()

#     if order_details:
#         return order_details

#     raise HTTPException(status_code=404, detail="Order Not Found")


# def search_order_by_cust_id(cust_id: int, db: Session):
#     order_details = db.query(Order).filter_by(cust_id=cust_id).all()

#     if order_details:
#         return order_details

#     raise HTTPException(status_code=404, detail="Order Not Found")




def get_order(db: Session):
    try:
        logger.info("Fetching all orders...")

        result = db.execute(text("SELECT * FROM orders ORDER BY order_id"))
        orders = result.fetchall()

        logger.info("Successfully fetched %d orders", len(orders))
        return orders

    except Exception:
        db.rollback()   # Optional for SELECT
        logger.error("Failed to fetch orders")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch orders"
        )


def search_order_by_order_id(ord_id: int, db: Session):
    try:
        logger.info("Searching order with Order ID: %s", ord_id)

        order = db.query(Order).filter_by(order_id=ord_id).first()

        if order is None:
            logger.warning("Order not found with Order ID: %s", ord_id)
            raise HTTPException(
                status_code=404,
                detail="Order not found"
            )

        logger.info(
            "Order found | Order ID: %s | Customer ID: %s | Order Date: %s | Status: %s | Total Amount: %s",
            order.order_id,
            order.cust_id,
            order.order_date,
            order.status,
            order.total_amount)

        return order

    except HTTPException:
        raise

    except Exception:
        db.rollback()
        logger.error("Failed to search order by Order ID")
        raise HTTPException(
            status_code=500,
            detail="Failed to search order"
        )


def search_order_by_cust_id(cust_id: int, db: Session):
    try:
        logger.info("Searching orders with Customer ID: %s", cust_id)

        orders = db.query(Order).filter_by(cust_id=cust_id).all()

        if not orders:
            logger.warning("No orders found for Customer ID: %s", cust_id)
            raise HTTPException(
                status_code=404,
                detail="No orders found for this customer"
            )

        logger.info(
            "Found %d order(s) for Customer ID: %s",
            len(orders),
            cust_id,
        )

        return orders

    except HTTPException:
        raise

    except Exception:
        db.rollback()
        logger.error("Failed to search orders by Customer ID")
        raise HTTPException(
            status_code=500,
            detail="Failed to search orders"
        )