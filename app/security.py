from pwdlib import PasswordHash
import os
import base64

password_hase=PasswordHash.recommended()


def hash_password(password:str)->str:
    return password_hase.hash(password)

def verify_password(plain_password:str,hashed_password:str)-> bool:
    return password_hase.verify(plain_password,hashed_password)