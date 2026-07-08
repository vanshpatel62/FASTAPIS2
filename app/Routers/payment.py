from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import Schemas, Services
from app.database import get_db

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)



# @router.get("/peyment",response_model=list[Schemas.payment])
# def get_payments(db:Session=Depends(get_db)):
#     return Services.get_payments_details(db)

from fastapi import HTTPException

@router.get("/peyment", response_model=list[Schemas.payment])
def get_payments(db: Session = Depends(get_db)):
    try:
        logger.info("Get All Payments API called")
        return Services.get_payments_details(db)

    except HTTPException:
        raise

    except Exception:
        logger.error("Get All Payments API failed")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )