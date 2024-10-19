import os

from alembic import command
from alembic.config import Config
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()
SQLALCHEMY_DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()

alembic_cfg = Config("alembic.ini")

if os.environ.get("ENV") == "dev":
    command.upgrade(alembic_cfg, "head")
    print("Alembic upgrade head")
    Base.metadata.create_all(bind=engine)
    print("Tables created")
