from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session

from app import Schemas, Services
from app.database import get_db

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/ordr_items",
    tags=["Order Items"]
)


@router.get("/order_items",response_model=list[Schemas.order_item])
def get_order_items(db:Session=Depends(get_db)):
    try:
        logger.info("Get All Order Items API called")
        return Services.get_order_items(db)

    except HTTPException:
        raise

    except Exception:
        logger.error("Get All Order Items API failed")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )