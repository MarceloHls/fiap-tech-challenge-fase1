import pandas as pd
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.models import Book, Base, UserDB

if not os.path.exists("data"):
    os.makedirs("data")

DATA_PATH = "data/books.csv"
DB_URL = "sqlite:///./data/users.db"

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_csv():
    if not os.path.exists(DATA_PATH):
        return None
    return pd.read_csv(DATA_PATH)

def get_db_as_objects():
    df = get_db_csv()
    if df is None: return []
    return [
        Book(id=int(i), title=r.title, price=r.price, rating=r.rating, 
             availability=r.availability, category=r.get('category', 'N/A'), 
             image_url=r.image_url) 
        for i, r in df.iterrows()
    ]

def get_book_by_id(book_id: int):
    all_books = get_db_as_objects()
    return next((b for b in all_books if b.id == book_id), None)

def get_user(db_session, username: str):

    return db_session.query(UserDB).filter(UserDB.username == username).first()

def create_user(db_session, username: str, hashed_password: str):
    db_user = UserDB(username=username, hashed_password=hashed_password)
    db_session.add(db_user)
    db_session.commit()
    db_session.refresh(db_user)
    return db_user

init_db()