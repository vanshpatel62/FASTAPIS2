# from pydantic import 
from fastapi import FastAPI,HTTPException,Depends,Request
from app import models
from app.models import Customer,Product,Order,Payment
from sqlalchemy.orm import Session
from app import schemas
from app.schemas import customer_data
from sqlalchemy import text


def create_customre(db: Session, data: schemas.add_customre):
    customer_ins = Customer(**data.model_dump())
    db.add(customer_ins)
    db.commit()
    db.refresh(customer_ins)
    return  customer_ins

def get_customre(db:Session):
    return db.query(Customer).all()

# search cutomer
def search_customer(cust_id:int,db:Session):
    cust_details=db.query(Customer).filter_by(cust_id=cust_id).all()

    if(cust_details):
        return cust_details
    else:
        raise HTTPException(status_code=404,detail="Customer Not Found")

# For update
def update_cust(cust_id:int,cust:schemas.customer_data,db:Session):
    find_cust=db.query(Customer).filter_by(cust_id=cust_id).first()
    if find_cust:
        for key,value in cust.model_dump().items():
            setattr(find_cust,key,value)
        db.commit()
        db.refresh(find_cust)
    return find_cust

def delet_cust(cust_id:int,db:Session):

    delete_cust=db.query(Customer).filter_by(cust_id=cust_id).first()
    if delete_cust is None:
        raise HTTPException(status_code=404,detail="Customer Can Not Found")
        
    else:
        db.delete(delete_cust)
        db.commit()
        return delete_cust


def get_product(db:Session):
    result=db.execute(text("select * from products order by p_id"))
    return result.fetchall()
    # return db.query(Product).all()


def search_product(p_id:int,db:Session):
    product_details=db.query(Product).filter_by(p_id=p_id).all()

    if (product_details):
        return product_details
    else:
        raise HTTPException(status_code=404,detail="Product Not Found")


def get_order(db:Session):
    # return db.query(Order).all()
    # or
    result=db.execute(text("select * from orders order by order_id"))
    return result.fetchall()

def search_order_by_order_id(ord_id:int,db:Session):
    order_deteils=db.query(Order).filter_by(order_id=ord_id).all()

    if (order_deteils):
        return order_deteils
    else:
        raise HTTPException(status_code=404,detail="Order Not Found")

def search_order_by_cust_id(cust_id:int,db:Session):
    order_deteils_=db.query(Order).filter_by(cust_id=cust_id).all()

    if(order_deteils_):
        return order_deteils_
    else:
        raise HTTPException(status_code=404,detail="Order Not Found")   


def get_order_items(db:Session):
    return db.query(models.OrderItem).all()

def get_payments_details(db:Session):
    return db.query(Payment).all()