from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

print("=" * 60)
print("DATABASE_URL =", DATABASE_URL)
print("=" * 60)

engine = create_engine(DATABASE_URL)

Base = declarative_base()
