# lib/models/platform.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, validates
from .base import Base, Session # Import Base and Session from base.py

class Platform(Base):
	__tablename__ = 'platforms'

	id = Column(Integer, primary_key=True)
	_name = Column("name", String, unique=True, nullable=False) # Backing field for property

	# Relationship: One Platform can have many Games
	games = relationship("Game", back_populates="platform")

	def __init__(self, name):
		self.name = name # Uses the setter

	@property
	def name(self):
		"""Getter for the platform name."""
		return self._name

	@name.setter
	def name(self, value):
		"""Setter for the platform name with validation."""
		if not isinstance(value, str):
			raise TypeError("Platform name must be a string.")
		if not 2 <= len(value) <= 50:
			raise ValueError("Platform name must be between 2 and 50 characters.")
		self._name = value

	# ORM Methods as required
	@classmethod
	def create(cls, session, name):
		"""Creates a new platform instance and adds it to the session."""
		try:
			platform = cls(name=name) # Uses the __init__ which triggers the setter
			session.add(platform)
			session.commit()
			return platform
		except (TypeError, ValueError) as e:
			session.rollback() # Rollback in case of validation error during creation
			print(f"Error creating platform: {e}")
			return None
		except Exception as e:
			session.rollback()
			print(f"An unexpected error occurred during platform creation: {e}")
			return None


	@classmethod
	def get_all(cls, session):
		"""Returns a list of all platforms."""
		return session.query(cls).all()

	@classmethod
	def find_by_id(cls, session, platform_id):
		"""Finds a platform by its ID."""
		return session.query(cls).get(platform_id)

	@classmethod
	def find_by_name(cls, session, name):
		"""Finds a platform by its name."""
		return session.query(cls).filter(cls._name == name).first()

	def update(self, session, name=None):
		"""Updates the platform's attributes."""
		if name is not None:
			try:
				self.name = name # Uses the setter for validation
				session.commit()
				return True
			except (TypeError, ValueError) as e:
				session.rollback()
				print(f"Error updating platform: {e}")
				return False
			except Exception as e:
				session.rollback()
				print(f"An unexpected error occurred during platform update: {e}")
				return False
		return False # No update performed if name is None

	def delete(self, session):
		"""Deletes the platform instance from the database."""
		# Basic check: ensure no games are associated before deleting, or handle cascade
		if self.games:
			print(f"Cannot delete platform '{self.name}' as it has associated games. Please reassign or delete those games first.")
			return False
		try:
			session.delete(self)
			session.commit()
			return True
		except Exception as e:
			session.rollback()
			print(f"Error deleting platform: {e}")
			return False

	def __repr__(self):
		return f"<Platform(id={self.id}, name='{self.name}')>"
