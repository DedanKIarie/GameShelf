# lib/models/genre.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base, Session

class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True)
    _name = Column("name", String, unique=True, nullable=False)

    games = relationship("Game", back_populates="genre")

    def __init__(self, name):
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Genre name must be a string.")
        if not 2 <= len(value) <= 30:
            raise ValueError("Genre name must be between 2 and 30 characters.")
        self._name = value

    @classmethod
    def create(cls, session, name):
        try:
            genre = cls(name=name)
            session.add(genre)
            session.commit()
            return genre
        except (TypeError, ValueError) as e:
            session.rollback()
            print(f"Error creating genre: {e}")
            return None
        except Exception as e:
            session.rollback()
            print(f"An unexpected error occurred: {e}")
            return None


    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, genre_id):
        return session.query(cls).get(genre_id)

    @classmethod
    def find_by_name(cls, session, name):
        return session.query(cls).filter(cls._name == name).first()

    def update(self, session, name=None):
        if name is not None:
            try:
                self.name = name
                session.commit()
                return True
            except (TypeError, ValueError) as e:
                session.rollback()
                print(f"Error updating genre: {e}")
                return False
        return False

    def delete(self, session):
        if self.games:
            print(f"Cannot delete genre '{self.name}' as it has associated games.")
            return False
        try:
            session.delete(self)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error deleting genre: {e}")
            return False

    def __repr__(self):
        return f"<Genre(id={self.id}, name='{self.name}')>"
