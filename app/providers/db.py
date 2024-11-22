import os

from databases import Database
from sqlalchemy import MetaData

metadata = MetaData()
DATABASE_HOST = os.getenv("DATABASE_HOST", "db")
DATABASE_PORT = os.getenv("DATABASE_PORT", "3306")
DATABASE_NAME = os.getenv("DATABASE_NAME", "chat")
DATABASE_USER = os.getenv("DATABASE_USER", "root")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "123456")
DATABASE_URL = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

db = Database(DATABASE_URL)
