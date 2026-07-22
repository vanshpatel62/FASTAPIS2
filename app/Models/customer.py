from app.database import Base
from sqlalchemy import Integer,String,Column,Text,TIMESTAMP,text,CheckConstraint,Numeric,ForeignKey,DECIMAL
from sqlalchemy.orm import relationship,Mapped,mapped_column
# data = data.model_dump()

class Customer(Base):
    __tablename__="customers"
    
    cust_id=Column(Integer,primary_key=True)
    name=Column(String(20),nullable=False)
    # email=Column(Text,unique=True,nullable=False)
    email: Mapped[str] = mapped_column(String,unique=True,nullable=False)
    city=Column(String(20))
    join_date=Column(TIMESTAMP,server_default=text("CURRENT_TIMESTAMP"))

    # rders = relationship("Order", back_populates="Customers")
    # customer = relationship("Customres", back_populates="orders")
    orders = relationship("Order", back_populates="customer")
 
    # __table_args__ = (
    #     CheckConstraint(
    #         r"email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'",
    #         name="customers_email_check",
    #     ),
    # )
