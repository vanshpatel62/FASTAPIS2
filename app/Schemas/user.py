from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict, Field

class get_user(BaseModel):
    user_id :int
    user_name :str
    mobile :str
    password :str
    role:str
    last_log_in :datetime

    model_config = ConfigDict(from_attributes=True)

class register_user(BaseModel):
    user_name :str
    mobile :str
    password :str
    role:str
    last_log_in :datetime 

class login(BaseModel):
    user_name:str
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str