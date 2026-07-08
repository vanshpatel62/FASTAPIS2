from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.Models import Payment

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_payments_details(db: Session):
    try:
        logger.info("Fetching all payments...")

        payments = db.query(Payment).all()

        logger.info(
            "Successfully fetched %d payment(s)",
            len(payments)
        )

        return payments

    except Exception:
        db.rollback()   # Optional for SELECT, but safe
        logger.error("Failed to fetch payments")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch payments"
        )