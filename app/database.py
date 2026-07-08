from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

import logging
logger = logging.getLogger(__name__)

DATABASE_URL = "postgresql+psycopg://postgres:0602@localhost:5432/db1"
# postgresql+psycopg://:password@host:port/database_name

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

# Base=DeclarativeBase()


def get_db():
    db=SessionLocal()
    # print("========== OPEN SESSION ==========")
    logger.info("✅ Database Session Opened")
    try:
        yield db
    finally:
        db.close()
        # print("========== CLOSE SESSION ==========")
        logger.info("❌ Database Session Closed")


class Base(DeclarativeBase):
    pass


try:
    with engine.connect() as connection:
        print("Database Connected Successfully!")
except Exception as e:
    print(e)