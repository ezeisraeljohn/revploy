from sqlmodel import Session, create_engine, SQLModel


DATABASE_URL = "sqlite:///database.db"

engine = create_engine(DATABASE_URL)


def get_db():
    """Create a session"""
    with Session(bind=engine, autoflush=False, autocommit=False) as session:
        yield session
