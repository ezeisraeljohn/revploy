from sqlmodel import Session, create_engine, SQLModel
import os
import pymysql
from dotenv import load_dotenv

pymysql.install_as_MySQLdb()

DATABASE_URL = os.getenv("DATABASE_URL")
CA_CERT_PATH = os.getenv("CA_CERT_PATH")

engine = create_engine(
    url=DATABASE_URL,
    connect_args={
        "ssl": {
            "sslmode": "REQUIRED",
            "ca": CA_CERT_PATH,
        },
    },
)


def get_db():
    """Create a session"""
    with Session(bind=engine, autoflush=False, autocommit=False) as session:
        yield session
