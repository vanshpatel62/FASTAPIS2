# from pydantic import BaseModel
from datetime import datetime,timezone,date
from decimal import Decimal
from pydantic import BaseModel, ConfigDict,Field

class customer_data(BaseModel):
    cust_id:int
    name:str
    email:str
    city:str
    join_date:datetime
    model_config = ConfigDict(from_attributes=True)

class add_customre(BaseModel):
    name:str
    email:str
    city:str
    # join_date: date = Field(default_factory=date)
    join_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    # join_date: datetime = Field(default_factory=datetime.utc)
    # join_date:datetime
    # model_config = ConfigDict(from_attributes=True)

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

class order_item(BaseModel):
    order_id :int
    items_id :int
    quantity :int
    unit_price : Decimal
 

class payment(BaseModel):
    payment_id : int
    transaction_id : str
    order_id : int
    amount : Decimal
    payment_method : str
    payment_date : datetime
    payment_status : str
    # model_config = ConfigDict(from_attributes=True)
    