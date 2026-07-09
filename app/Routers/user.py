from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session

from app import Schemas, Services
from app.database import get_db
import logging
import hashlib


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

@router.get("/user",response_model=list[Schemas.get_user])
def show_details(db:Session=Depends(get_db)):
    try:
        logger.info("Get User Details API called")
        return Services.get_details(db)

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Get User Details API failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )


@router.post("/add_user",response_model=Schemas.register_user)
def add_user(user_info:Schemas.register_user,db:Session=Depends(get_db)):
    try:
        logger.info("Create User API called")

        user = Services.create_user(db, user_info)

        logger.info(f"User created successfully | ID: {user.user_id}")
        return user

    except HTTPException:
        raise

    except Exception as e:
        logger.exception(f"Error creating user: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )
    

@router.post("/login",response_model=Schemas.login)
def user_login(data:Schemas.login,db:Session=Depends(get_db)):

    try:
        logger.info("Login API called")
        user = Services.user_login(db, data)
        logger.info(f"Login API completed successfully | User Name: {user.user_name}")
        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error during login: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )