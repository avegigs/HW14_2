from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from fastapi import Depends
from database.database import SessionLocal
from database.models import Base

def get_test_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_test_database(db: Session):
    Base.metadata.create_all(bind=db.bind)

def drop_test_database(db: Session):
    for table in reversed(Base.metadata.sorted_tables):
        db.execute(table.delete())
    db.commit()
