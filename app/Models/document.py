from app.database import Base
from sqlalchemy import Integer,String,text,TIMESTAMP,ForeignKey,CheckConstraint,DateTime,func
from sqlalchemy.orm import Mapped,mapped_column



class Document(Base):
    __tablename__="documents"

    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    user_id:Mapped[int]=mapped_column(Integer,ForeignKey("customers.cust_id"),nullable=False)
    email:Mapped[str]=mapped_column(String,nullable=False)
    email_lookup:Mapped[str]=mapped_column(String,nullable=False)
    doc_type:Mapped[str | None]=mapped_column(String)
    doc_path:Mapped[str| None]=mapped_column(String)
    save_time:Mapped[DateTime | None]=mapped_column(DateTime,server_default=func.current_timestamp())  