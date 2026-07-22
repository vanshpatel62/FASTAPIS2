import os
import base64
import hmac
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from app.utils.key_manager import AES_KEY

aesgcm = AESGCM(AES_KEY)

def encrypt(plaintext:str)->str:

    nonce=os.urandom(12)

    ciphertext=aesgcm.encrypt(
        nonce,
        plaintext.encode(),
        None
    )

    return base64.b64encode(nonce+ciphertext).decode()

def decrypt(ciphertext:str)->str:

    data=base64.b64decode(ciphertext)

    nonce=data[:12]
    encrypt=data[12:]

    plaintext=aesgcm.decrypt(nonce,encrypt,None)

    return plaintext.decode()

