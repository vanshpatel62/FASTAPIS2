# from pydantic import 
from app.models import Customer,Product,Order
from sqlalchemy.orm import Session
from app.schemas import customer_data
from sqlalchemy import text

# def create_customre(db:Session,gd:customer_data):
#     data = gd.model_dump()
#     customer_ins=Customres(data)

# 
def create_customre(db: Session, data: customer_data):
    customer_ins = Customer(**data.model_dump())
    db.add(customer_ins)
    db.commit()
    db.refresh(customer_ins)
    return  customer_ins

def get_customre(db:Session):
    return db.query(Customer).all()


def get_product(db:Session):
    result=db.execute(text("select * from products order by p_id"))
    return result.fetchall()
    # return db.query(Product).all()

def get_order(db:Session):
    result=db.execute(text("select * from orders order by order_id"))
    # return db.query(Order).all()
    return result.fetchall()