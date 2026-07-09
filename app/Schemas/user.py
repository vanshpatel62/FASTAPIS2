from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict, Field

class get_user(BaseModel):
    user_id :int
    user_name :str
    mobile :str
    password :str
    role:str
    last_log_in :datetime 

class register_user(BaseModel):
    user_name :str
    mobile :str
    password :str
    role:str
    last_log_in :datetime 

class login(BaseModel):
    user_name:str
    password:str