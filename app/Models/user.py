from app.database import Base
from sqlalchemy import Integer,String,Column,Text,TIMESTAMP,text,CheckConstraint,Numeric,ForeignKey,DECIMAL
# from sqlalchemy.orm import relationship

class User(Base):
    __tablename__="users"

    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(100), nullable=False)
    mobile = Column(String(15), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default="customer")
    last_log_in = Column(TIMESTAMP, nullable=True)

     

    __table_args__ = (
        CheckConstraint(
            "role IN ('customer', 'admin')",
            name="chk_user_role"
        ),
    )

