from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import Schemas, Services
from app.database import get_db

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)



# @router.get("/products",response_model=list[Schemas.produsts_data])
# def get_produsts(db:Session=Depends(get_db)):
#     return Services.get_product(db)

# @router.get("/produsts/{product_id}",response_model=list[Schemas.produsts_data])
# def search_product(product_id:int,db:Session=Depends(get_db)):
#     return Services.search_product(product_id,db)



from fastapi import HTTPException

@router.get("/products", response_model=list[Schemas.produsts_data])
def get_produsts(db: Session = Depends(get_db)):
    try:
        logger.info("Get All Products API called")
        return Services.get_product(db)

    except HTTPException:
        raise

    except Exception:
        logger.error("Get All Products API failed")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )


@router.get("/products/{product_id}", response_model=Schemas.produsts_data)
def search_product(product_id: int, db: Session = Depends(get_db)):
    try:
        logger.info("Search Product API called")
        return Services.search_product(product_id, db)

    except HTTPException:
        raise

    except Exception:
        logger.error("Search Product API failed")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )