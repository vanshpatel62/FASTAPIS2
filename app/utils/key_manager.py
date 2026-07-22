import os
import base64
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("AES_KEY")

if key is None:
    raise ValueError("AES_KEY not found in .env file")

AES_KEY=base64.b64decode(key)

if len(AES_KEY) != 32:
    raise ValueError("AES_KEY must be 32 bytes.")




hmac_key = os.getenv("HMAC_KEY")

if hmac_key is None:
    raise ValueError("HMAC_KEY not found in .env file")

HMAC_KEY = base64.b64decode(hmac_key)

if len(HMAC_KEY) != 32:
    raise ValueError("HMAC_KEY must be 32 bytes.")