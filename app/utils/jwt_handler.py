from jose import jwt,JWTError
from datetime import datetime,timedelta,timezone
from typing import cast,Any
import logging
logger = logging.getLogger(__name__)

from app.config import (SECRET_KEY,ALGORITHM,ACCESS_TOKEN_EXPIRE_SECONDS)

def create_access_token(data:dict[str, Any])-> str:
    to_encode=data.copy()

    expiry=datetime.now(timezone.utc)+timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS)

    to_encode.update({
        "exp":expiry
    })

    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token:str):
    try:
        print("TOKEN =", token)
        
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])

        print("PAYLOAD =", payload)
        return payload
    
    except JWTError as e:
        logger.info(f"are you not valid for this for reasion of -->{e}")
        return None