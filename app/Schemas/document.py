from datetime import datetime,timezone
from pydantic import BaseModel,ConfigDict,Field
from typing import Optional

class document(BaseModel):
    id:int
    user_id:int
    email:str
    doc_type: Optional[str] = None
    doc_path: Optional[str]=None
    save_time: Optional[datetime]=None

class set_document(BaseModel):
    user_id:int
    email:str
    email_lookup:str
    doc_type:str
    doc_pat:str
    save_time:datetime

class set_registration(BaseModel):
    user_id: int
    email: str