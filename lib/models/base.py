from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///gameshelf.db" 
engine = create_engine(DATABASE_URL) 
Session = sessionmaker(bind=engine)
Base = declarative_base()