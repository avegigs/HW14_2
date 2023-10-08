from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

engine = create_engine(os.getenv("DATABASE_URL"))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Створює об'єкт сесії бази даних та надає його як залежність для інших функцій.

    Yields:
        Session: Об'єкт сесії бази даних.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
