from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.Models import Product

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# def get_product(db: Session):
#     result = db.execute(text("select * from products order by p_id"))
#     return result.fetchall()


# def search_product(p_id: int, db: Session):
#     product_details = db.query(Product).filter_by(p_id=p_id).all()

#     if product_details:
#         return product_details

#     raise HTTPException(status_code=404, detail="Product Not Found")



def get_product(db: Session):
    try:
        logger.info("Fetching all products...")

        result = db.execute(text("SELECT * FROM products ORDER BY p_id"))
        products = result.fetchall()

        logger.info("Successfully fetched %d products", len(products))
        return products

    except Exception:
        db.rollback()   # Optional for SELECT, but safe
        logger.error("Failed to fetch products")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch products"
        )


def search_product(p_id: int, db: Session):
    try:
        logger.info("Searching product with ID: %s", p_id)

        product = db.query(Product).filter_by(p_id=p_id).first()

        if product is None:
            logger.warning("Product not found with ID: %s", p_id)
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        logger.info(
            "Product found | ID: %s | Name: %s | Price: %s | Stock: %s",
            product.p_id,
            product.p_name,
            product.price,
            product.stock,
        )

        return product

    except HTTPException:
        raise

    except Exception:
        db.rollback()   # Optional for SELECT, but safe
        logger.error("Failed to search product")
        raise HTTPException(
            status_code=500,
            detail="Failed to search product"
        )