from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///gameshelf.db" # Local SQLite database file
engine = create_engine(DATABASE_URL) # echo=True can be useful for debugging SQL
Session = sessionmaker(bind=engine)
Base = declarative_base()