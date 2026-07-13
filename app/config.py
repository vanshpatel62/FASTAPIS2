from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

SECRET_KEY=os.getenv("SECRET_KEY","ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$_`~%^&*()")
ALGORITHM=os.getenv("ALGORITHM","HS512")
ACCESS_TOKEN_EXPIRE_SECONDS=int(os.getenv("ACCESS_TOKEN_EXPIRE_SECONDS",30))
