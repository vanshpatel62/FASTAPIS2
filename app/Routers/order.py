from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session

from app import Schemas, Services
from app.database import get_db

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


# @router.get("/orders",response_model=list[Schemas.orders_data])
# def get_orders(db:Session=Depends(get_db)):
#     return Services.get_order(db)

# @router.get("/orders/{ord_id}",response_model=list[Schemas.orders_data])
# def search_orders_by_ord_id(ord_id: int,db: Session = Depends(get_db)):
#     return Services.search_order_by_order_id(ord_id,db)

# @router.get("/orders_by_cust_id/{cust_id}",response_model=list[Schemas.orders_data])
# def search_orders_by_cust_id(cust_id: int,db: Session = Depends(get_db)):
#     return Services.search_order_by_cust_id(cust_id,db)




@router.get("/orders", response_model=list[Schemas.orders_data])
def get_orders(db: Session = Depends(get_db)):
    try:
        logger.info("Get All Orders API called")
        return Services.get_order(db)

    except HTTPException:
        raise

    except Exception:
        logger.error("Get All Orders API failed")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )


@router.get("/orders/{ord_id}", response_model=Schemas.orders_data)
def search_orders_by_ord_id(ord_id: int, db: Session = Depends(get_db)):
    try:
        logger.info("Search Order by Order ID API called")
        return Services.search_order_by_order_id(ord_id, db)

    except HTTPException:
        raise

    except Exception:
        logger.error("Search Order by Order ID API failed")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )


@router.get("/orders_by_cust_id/{cust_id}", response_model=list[Schemas.orders_data])
def search_orders_by_cust_id(cust_id: int, db: Session = Depends(get_db)):
    try:
        logger.info("Search Orders by Customer ID API called")
        return Services.search_order_by_cust_id(cust_id, db)

    except HTTPException:
        raise

    except Exception:
        logger.error("Search Orders by Customer ID API failed")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )