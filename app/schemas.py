# from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict

class customer_data(BaseModel):
    cust_id:int
    name:str
    email:str
    city:str
    join_date:datetime
    model_config = ConfigDict(from_attributes=True)

# class customre()

class produsts_data(BaseModel):
    p_id:int
    p_name:str
    category:str
    price:int
    stock:int
    brand:str

class orders_data(BaseModel):
    order_id:int
    cust_id:int
    order_date:datetime
    status:str
    total_amount:Decimal

    model_config = ConfigDict(from_attributes=True)