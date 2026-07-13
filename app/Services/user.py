from fastapi import HTTPException,Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from app import Schemas,Models
from typing import cast
from app.Models import User
import logging
from app import security
from app.utils.jwt_handler import create_access_token
from app.dependencies import get_current_user


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



def get_details(db: Session):
    try:
        logger.info("Fetching all users")
        users = db.query(Models.User).all()
        logger.info(f"Fetched {len(users)} users")
        return users
    except Exception as e:
        logger.exception(f"Error fetching users: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )


def create_user(db: Session, user_info: Schemas.register_user):
    try:
        logger.info("Creating new user ")

        # hashed_pwd = hashlib.md5(
        #     user_info.password.encode("utf-8")
        # ).hexdigest()

        user_info.password = security.hash_password(user_info.password)

        new_user = Models.User(
            user_name=user_info.user_name,
            mobile=user_info.mobile,
            password=user_info.password,
            role=user_info.role,
            last_log_in=user_info.last_log_in
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        logger.info(f"User created successfully | ID: {new_user.user_id}")
        return new_user

    except IntegrityError as e:
        db.rollback()
        logger.warning(f"Duplicate mobile number: {user_info.mobile} | {e}")
        raise HTTPException(
            status_code=400,
            detail="User with this mobile number already exists"
        )
    except Exception as e:
        db.rollback()
        logger.exception(f"Database error while creating user: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )
    
def user_login(db:Session,id_pass:Schemas.login):
    
    # hashed_pwd = hashlib.md5(id_pass.password.encode("utf-8")).hexdigest()
    try:

        user_ = db.query(Models.User).filter_by(user_name = id_pass.user_name).first()

        if not user_:
            logger.warning(f"Login failed - user  {id_pass.user_name} is not found:")
            raise HTTPException(
                status_code=401,
                detail="Invalid user name  or password")


        # hashed_input_pwd = hashlib.md5(
        #         id_pass.password.encode("utf-8")
        #     ).hexdigest()



        if not security.verify_password(id_pass.password,cast(str,user_.password)) :
            logger.warning(f"Login failed - wrong password for : {id_pass.user_name}")
            raise HTTPException(
                status_code=401,
                detail="Invalid user name or password")
        
        
        
        token = create_access_token(
            {"sub": user_.user_name,
            "user_id": user_.user_id,
            "role": user_.role
                })

        user_.last_log_in = datetime.now()  # type: ignore[assignment]
        db.commit()

        
        # user.last_log_in = datetime.utcnow()
        # user.last_log_in = datetime.now(timezone.utc)

        user_.last_log_in = datetime.now()  # type: ignore[assignment]
        db.commit()
        db.refresh(user_)

        logger.info(f"Login successful | User ID: {user_.user_id}")
        return {
            "access_token":token,
            "token_type":"bearer"
        }
        # return user_
    
    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        logger.exception(f"Database error during login: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )
    
def delete_user(user_id:int,db:Session):
    try:

        user=db.query(User).filter_by(user_id=user_id).first()

        if user is None:
                logger.warning("User not found with ID: %s", user_id)
                raise HTTPException(
                    status_code=404,
                    detail="Customer not found"
                )
        
        db.delete(user)
        db.commit()

        logger.info(
                "Customer found | \n|ID: %s \n| Name: %s \n| Mobile: %s \n| Role: %s",
                user.user_id,
                user.user_name,
                user.mobile,
                user.role
            )

        return user
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Faild to fatch user")
        raise HTTPException(status_code=500,detail="Faild to Delete user")
    
def search_user(user_id: int, db: Session):

    user = db.query(Models.User).filter(
        Models.User.user_id == user_id
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user

def get_admin_user(current_user=Depends(get_current_user)):
        
    if current_user['role']!="admin":
        raise HTTPException(status_code=403,detail="Only Admin Can Access This API")
    
    return current_user