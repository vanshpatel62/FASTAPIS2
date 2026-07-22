from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import cast
from app import Schemas
from app.Models import Customer
import logging
from app.utils.encryption import encrypt,decrypt
from app.utils.lookup import encrypt_hash
# from utils import encryption

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_customre(db: Session, data: Schemas.add_customre):
    try:
        logger.info("           Creating new Customer...")

        # customer_ins = Customer(**data.model_dump())
        customer_ins=data.model_dump()
        customer_ins['email']=encrypt(customer_ins['email'])
        customer_ins = Customer(**customer_ins)

        db.add(customer_ins)
        db.commit()
        db.refresh(customer_ins)

        logger.info(
            "Customer created successfully | \n |ID: %s \n| Name: %s \n| Email: %s \n| City: %s \n| Join Date: %s",
            customer_ins.cust_id,
            customer_ins.name,
            (customer_ins.email),
            customer_ins.city,
            customer_ins.join_date
            )
        return customer_ins
    
    except Exception as e:
        db.rollback()
        logger.error("          Faild to create customer %s",e)
        raise HTTPException(status_code=500,detail="Faild to create customer")



def get_customre(db: Session):
    try:
        logger.info("           Fetching all customers from the database ...")

        customers = db.query(Customer).all()

        for customer in customers:
            customer.email = decrypt(customer.email)           

        logger.info("           Successfully fetched %d customers", len(customers))
        return customers

    except Exception:
        logger.exception("          Failed to fetch customers from the database")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )
    


def search_customer(cust_id: int, db: Session):
    try:
        logger.info("Searching customer with ID: %s", cust_id)

        customer = db.query(Customer).filter_by(cust_id=cust_id).first()

        if customer is None:
            logger.warning("Customer not found with ID: %s", cust_id)
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )
        customer.email = decrypt(customer.email)

        logger.info(
            "Customer found | \n|ID: %s \n| Name: %s \n| Email: %s \n| City: %s \n| Join Date: %s",
            customer.cust_id,
            customer.name,
            customer.email,
            customer.city,
            customer.join_date,
        )

        return customer

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()   # Optional for SELECT, but safe
        logger.error("Failed to search customer %s",e)
        raise HTTPException(
            status_code=500,
            detail="Failed to search customer"
        )


def update_cust(cust_id: int, cust: Schemas.customer_data, db: Session):
    # find_cust = db.query(Customer).filter_by(cust_id=cust_id).first()

    # if find_cust:
    #     for key, value in cust.model_dump().items():
    #         setattr(find_cust, key, value)

    #     db.commit()
    #     db.refresh(find_cust)

    # return find_cust
    try:
        logger.info("Updating customer with ID: %s", cust_id)

        find_cust = db.query(Customer).filter_by(cust_id=cust_id).first()
        
        if find_cust is None:
            logger.warning("Customer not found with ID: %s", cust_id)
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )
        
        # old_data = {
        #     "name": find_cust.name,
        #     "email": find_cust.email,
        #     "city": find_cust.city,
        #     "join_date": find_cust.join_date,
        # }

        logger.info(
            "Customer Old Data | \n|ID: %s \n| Name: %s \n| Email: %s \n| City: %s \n| Join Date: %s",
            find_cust.cust_id,
            find_cust.name,
            decrypt(find_cust.email),
            find_cust.city,
            find_cust.join_date,
        )

        update_data = cust.model_dump(exclude_unset=True)

        # Encrypt sensitive fields if present
        if "email" in update_data:
            update_data["email"] = encrypt(update_data["email"])

        for key, value in cust.model_dump().items():
            setattr(find_cust, key, value)

        db.commit()
        db.refresh(find_cust)

        logger.info(
            "Customer Updated Data | \n|ID: %s \n| Name: %s \n| Email: %s \n| City: %s \n| Join Date: %s",
            find_cust.cust_id,
            find_cust.name,
            decrypt(find_cust.email),
            find_cust.city,
            find_cust.join_date,
        )

        return find_cust

    except HTTPException:
        raise

    except IntegrityError:
        db.rollback()
        logger.error("Failed to update customer. Email already exists.")
        raise HTTPException(
            status_code=409,
            detail="Email already exists."
        )

    except Exception:
        db.rollback()
        logger.error("Failed to update customer")
        raise HTTPException(
            status_code=500,
            detail="Failed to update customer"
        )

def delet_cust(cust_id: int, db: Session):
    # delete_cust = db.query(Customer).filter_by(cust_id=cust_id).first()

    # if delete_cust is None:
    #     raise HTTPException(status_code=404, detail="Customer Can Not Found")

    # db.delete(delete_cust)
    # db.commit()

    # return delete_cust

    try:
        logger.info("Deleting customer with ID: %s", cust_id)

        delete_cust = db.query(Customer).filter_by(cust_id=cust_id).first()

        if delete_cust is None:
            logger.warning("Customer not found with ID: %s", cust_id)
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        db.delete(delete_cust)
        db.commit()

        logger.info(
            "Customer found | \n|ID: %s \n| Name: %s \n| Email: %s \n| City: %s \n| Join Date: %s",
            delete_cust.cust_id,
            delete_cust.name,
            decrypt(delete_cust.email),
            delete_cust.city,
            delete_cust.join_date,
        )

        return delete_cust

    except HTTPException:
        raise

    except Exception:
        db.rollback()
        logger.error("Failed to delete customer")
        raise HTTPException(
            status_code=500,
            detail="Failed to delete customer"
        )