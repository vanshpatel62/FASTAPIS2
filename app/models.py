from app.database import Base
from sqlalchemy import Integer,String,Column,Text,TIMESTAMP,text,CheckConstraint,Numeric,ForeignKey,DECIMAL
from sqlalchemy.orm import relationship
# data = data.model_dump()

class Customer(Base):
    __tablename__="customers"
    cust_id=Column(Integer,primary_key=True)
    name=Column(String(20),nullable=False)
    email=Column(Text,unique=True,nullable=False)
    city=Column(String(20))
    join_date=Column(TIMESTAMP,server_default=text("CURRENT_TIMESTAMP"))

    # rders = relationship("Order", back_populates="Customers")
    # customer = relationship("Customres", back_populates="orders")
    orders = relationship("Order", back_populates="customer")
 
    __table_args__ = (
        CheckConstraint(
            r"email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'",
            name="customers_email_check",
        ),
    )



    # orders = relationship("Order", back_populates="customer")
    # order_items = relationship("OrderItem", back_populates="product")
    # customer = relationship("Customer", back_populates="orders")
    # items = relationship("OrderItem", back_populates="order")
    # payment = relationship("Payment", back_populates="order", uselist=False)
    # order = relationship("Order", back_populates="items")
    # product = relationship("Product", back_populates="order_items")
    # order = relationship("Order", back_populates="payment")



    # ---------------------------- Products ------------------------------------


class Product(Base):
    __tablename__ = "products"
 
    p_id = Column(Integer, primary_key=True)
    p_name = Column(String(50), nullable=False)
    category = Column(String(20))
    price = Column(Numeric(8, 2))
    stock = Column(Integer)
    brand = Column(String(20))
 
    order_items = relationship("OrderItem", back_populates="product")
 
    __table_args__ = (
        CheckConstraint("price > 0", name="products_price_check"),
        CheckConstraint("stock >= 0", name="products_stock_check"),
    )
  


# ---------------------------------- Orders Table--------------------------------------------
class Order(Base):
    __tablename__ = "orders"
 
    order_id = Column(Integer, primary_key=True)
    cust_id = Column(Integer, ForeignKey("customers.cust_id"), nullable=False)
    order_date = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    status = Column(String(10), nullable=False)
    total_amount = Column(Numeric(8, 2), nullable=False)
 
    # customer = relationship("Customer", back_populates="orders")
    customer = relationship("Customer", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")
    payment = relationship("Payment", back_populates="order", uselist=False)
 
    __table_args__ = (
        CheckConstraint(
            "status IN ('Pending', 'Shipped', 'Delivered', 'Cancelled')",
            name="orders_status_check",
        ),
        CheckConstraint("total_amount >= 0", name="orders_total_amount_check"),
    )

    # ------------------------------------- Order_items Table-----------------------------------
class OrderItem(Base):
    __tablename__ = "order_items"
 
    order_id = Column(Integer, ForeignKey("orders.order_id"), primary_key=True)
    items_id = Column(Integer, ForeignKey("products.p_id"), primary_key=True)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(8, 2))
 
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
 
    __table_args__ = (
        CheckConstraint("quantity > 0", name="order_items_quantity_check"),
        CheckConstraint("unit_price > 0", name="order_items_unit_price_check"),
    )


    # ----------------------------------------------------------------

class Payment(Base):
    __tablename__ = "payments"
 
    payment_id = Column(Integer, primary_key=True)
    transaction_id = Column(Text, nullable=False, unique=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False, unique=True)
    amount = Column(Numeric(8, 2))
    payment_method = Column(String(20))
    payment_date = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    payment_status = Column(String(15))
 
    order = relationship("Order", back_populates="payment")
 
    __table_args__ = (
        CheckConstraint("amount > 0", name="payments_amount_check"),
        CheckConstraint(
            "payment_method IN ('Card', 'UPI', 'Cash')",
            name="payments_method_check",
        ),
        CheckConstraint(
            "payment_status IN ('Successfully', 'Pending', 'Cancelled')",
            name="payments_status_check",
        ),
    )