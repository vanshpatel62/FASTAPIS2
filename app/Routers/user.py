from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session

from app import Schemas, Services
from app.database import get_db
import logging
import hashlib
from app.dependencies import get_current_user
from fastapi.security import OAuth2PasswordRequestForm

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

@router.post("/login",response_model=Schemas.Token)
def user_login(data:Schemas.login,db:Session=Depends(get_db)):

    try:
        logger.info("Login API called")
        token = Services.user_login(db, data)
        logger.info(f"Login API completed successfully | User Name: {data.user_name}")
        # return user
        return token
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error during login: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )

@router.delete("/delete_user/{user_id}",response_model=Schemas.get_user)
def delete_user(user_id:int,db:Session=Depends(get_db),admin=Depends(Services.get_admin_user)):
    try:
        logger.info(f"Delete Api calling for ID:  {user_id}")
        return Services.delete_user(user_id,db)
    except  HTTPException:
        raise
    except Exception as e:
        logger.error("Delete api for user is faild")
        raise HTTPException(status_code=500,detail="Internal server error")
    


@router.get(
    "/search/{user_id}",
    response_model=Schemas.get_user
)
def search_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return Services.search_user(user_id, db)


# @router.get("/userss",response_model=Schemas.get_user)
# def show_detailss(data=Depends(get_current_user)):
#     return data


# @router.post("/loginn",response_model=Schemas.Token)
# def user_loginn(data:Schemas.login,db:Session=Depends(get_db)):
#     return Services.user_login(db,data)



# @router.get("/profile",response_model=Schemas.get_user)
# def profile(current_user = Depends(get_current_user)):
#     return {
#         "message":"Welcome",

#         "user":current_user
#     }