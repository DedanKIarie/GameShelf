from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base, Session 

class Developer(Base):
    __tablename__ = 'developers'

    id = Column(Integer, primary_key=True)
    _name = Column("name", String, unique=True, nullable=False) 

 
    games = relationship("Game", back_populates="developer")

    def __init__(self, name):
        self.name = name 

    @property
    def name(self):
        """Getter for the developer name."""
        return self._name

    @name.setter
    def name(self, value):
        """Setter for the developer name with validation."""
        if not isinstance(value, str):
            raise TypeError("Developer name must be a string.")
        if not 2 <= len(value) <= 100: 
            raise ValueError("Developer name must be between 2 and 100 characters.")
        self._name = value


    @classmethod
    def create(cls, session, name):
        """Creates a new developer instance and adds it to the session."""
        try:
            developer = cls(name=name)
            session.add(developer)
            session.commit()
            return developer
        except (TypeError, ValueError) as e:
            session.rollback()
            print(f"Error creating developer: {e}")
            return None
    @classmethod
    def get_all(cls, session):
        """Returns a list of all developers."""
        return session.query(cls).order_by(cls._name).all()

    @classmethod
    def find_by_id(cls, session, developer_id):
        """Finds a developer by its ID."""
        return session.query(cls).get(developer_id)

    @classmethod
    def find_by_name(cls, session, name):
        """Finds a developer by its name."""
        return session.query(cls).filter(cls._name == name).first()

    def update(self, session, name=None):
        """Updates the developer's attributes."""
        if name is not None:
            try:
                self.name = name 
                session.commit()
                return True
            except (TypeError, ValueError) as e:
                session.rollback()
                print(f"Error updating developer: {e}")
                return False
        return False

    def delete(self, session):
        """Deletes the developer instance from the database."""
        if self.games:
            print(f"Cannot delete developer '{self.name}' as it has associated games. Please reassign or delete those games first.")
            return False
        try:
            session.delete(self)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error deleting developer: {e}")
            return False

    def __repr__(self):
        return f"<Developer(id={self.id}, name='{self.name}')>"
