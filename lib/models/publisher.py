# lib/models/publisher.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base, Session # Import Base and Session from base.py

class Publisher(Base):
    __tablename__ = 'publishers'

    id = Column(Integer, primary_key=True)
    _name = Column("name", String, unique=True, nullable=False) # Backing field for property

    # Relationship: One Publisher can publish many Games
    games = relationship("Game", back_populates="publisher")

    def __init__(self, name):
        self.name = name # Uses the setter

    @property
    def name(self):
        """Getter for the publisher name."""
        return self._name

    @name.setter
    def name(self, value):
        """Setter for the publisher name with validation."""
        if not isinstance(value, str):
            raise TypeError("Publisher name must be a string.")
        if not 2 <= len(value) <= 100:
            raise ValueError("Publisher name must be between 2 and 100 characters.")
        self._name = value

    # ORM Methods
    @classmethod
    def create(cls, session, name):
        """Creates a new publisher instance and adds it to the session."""
        try:
            publisher = cls(name=name)
            session.add(publisher)
            session.commit()
            return publisher
        except (TypeError, ValueError) as e:
            session.rollback()
            print(f"Error creating publisher: {e}")
            return None
        except Exception as e:
            session.rollback()
            print(f"An unexpected error occurred during publisher creation: {e}")
            return None

    @classmethod
    def get_all(cls, session):
        """Returns a list of all publishers."""
        return session.query(cls).order_by(cls._name).all()

    @classmethod
    def find_by_id(cls, session, publisher_id):
        """Finds a publisher by its ID."""
        return session.query(cls).get(publisher_id)

    @classmethod
    def find_by_name(cls, session, name):
        """Finds a publisher by its name."""
        return session.query(cls).filter(cls._name == name).first()

    def update(self, session, name=None):
        """Updates the publisher's attributes."""
        if name is not None:
            try:
                self.name = name # Uses the setter for validation
                session.commit()
                return True
            except (TypeError, ValueError) as e:
                session.rollback()
                print(f"Error updating publisher: {e}")
                return False
            except Exception as e:
                session.rollback()
                print(f"An unexpected error occurred: {e}")
                return False
        return False

    def delete(self, session):
        """Deletes the publisher instance from the database."""
        if self.games:
            print(f"Cannot delete publisher '{self.name}' as it has associated games. Please reassign or delete those games first.")
            return False
        try:
            session.delete(self)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error deleting publisher: {e}")
            return False

    def __repr__(self):
        return f"<Publisher(id={self.id}, name='{self.name}')>"
