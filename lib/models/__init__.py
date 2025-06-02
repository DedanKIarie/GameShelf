# lib/models/__init__.py

# Import Base, engine, and Session from base.py so they can be accessed via lib.models
from .base import Base, engine, Session

# Import all model classes to make them easily accessible
from .platform import Platform
from .genre import Genre
from .developer import Developer
from .publisher import Publisher
from .game import Game

def create_tables():
    """Creates all tables in the database."""
    print("Creating database tables if they don't exist...")
    Base.metadata.create_all(engine)
    print("Database tables created (or already exist).")

__all__ = [
    'Base', 'engine', 'Session', 'create_tables',
    'Platform', 'Genre', 'Developer', 'Publisher', 'Game'
]
