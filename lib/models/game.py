# lib/models/game.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, Session # Import Base and Session from base.py
# Import related models for type hinting and relationship definitions
from .platform import Platform
from .genre import Genre
from .developer import Developer
from .publisher import Publisher

class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    _title = Column("title", String, nullable=False)
    _release_year = Column("release_year", Integer) # Optional
    _rating = Column("rating", Integer) # Optional, e.g., 1-5 or 1-10

    # Foreign Keys
    platform_id = Column(Integer, ForeignKey('platforms.id'), nullable=False)
    genre_id = Column(Integer, ForeignKey('genres.id'), nullable=False)
    developer_id = Column(Integer, ForeignKey('developers.id'), nullable=True) # A game might have an unknown dev initially
    publisher_id = Column(Integer, ForeignKey('publishers.id'), nullable=True) # Or unknown publisher

    # Relationships (Many-to-One)
    platform = relationship("Platform", back_populates="games")
    genre = relationship("Genre", back_populates="games")
    developer = relationship("Developer", back_populates="games")
    publisher = relationship("Publisher", back_populates="games")

    def __init__(self, title, platform, genre, release_year=None, rating=None, developer=None, publisher=None):
        self.title = title # Uses setter
        self.platform = platform # Direct assignment, assumes valid Platform object
        self.genre = genre       # Direct assignment, assumes valid Genre object
        self.release_year = release_year # Uses setter
        self.rating = rating     # Uses setter
        self.developer = developer # Direct assignment
        self.publisher = publisher # Direct assignment

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str):
            raise TypeError("Game title must be a string.")
        if not 1 <= len(value) <= 150:
            raise ValueError("Game title must be between 1 and 150 characters.")
        self._title = value

    @property
    def release_year(self):
        return self._release_year

    @release_year.setter
    def release_year(self, value):
        if value is not None:
            if not isinstance(value, int):
                raise TypeError("Release year must be an integer.")
            # A simple year range validation
            if not (1950 <= value <= 2077): # Arbitrary reasonable range
                raise ValueError("Release year seems invalid.")
        self._release_year = value

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if value is not None:
            if not isinstance(value, int):
                raise TypeError("Rating must be an integer.")
            if not (1 <= value <= 5): # Assuming a 1-5 rating scale
                raise ValueError("Rating must be between 1 and 5.")
        self._rating = value

    # ORM Methods
    @classmethod
    def create(cls, session, title, platform, genre, release_year=None, rating=None, developer=None, publisher=None):
        """Creates a new game instance."""
        # Ensure platform and genre are actual objects, not just IDs, for the constructor
        if not isinstance(platform, Platform):
            raise TypeError("Invalid Platform object provided for Game creation.")
        if not isinstance(genre, Genre):
            raise TypeError("Invalid Genre object provided for Game creation.")
        if developer and not isinstance(developer, Developer):
            raise TypeError("Invalid Developer object provided for Game creation.")
        if publisher and not isinstance(publisher, Publisher):
            raise TypeError("Invalid Publisher object provided for Game creation.")

        try:
            game = cls(
                title=title, platform=platform, genre=genre,
                release_year=release_year, rating=rating,
                developer=developer, publisher=publisher
            )
            session.add(game)
            session.commit()
            return game
        except (TypeError, ValueError) as e:
            session.rollback()
            print(f"Error creating game: {e}")
            return None
        except Exception as e:
            session.rollback()
            print(f"An unexpected error occurred during game creation: {e}")
            return None

    @classmethod
    def get_all(cls, session):
        """Returns a list of all games."""
        return session.query(cls).order_by(cls._title).all()

    @classmethod
    def find_by_id(cls, session, game_id):
        """Finds a game by its ID."""
        return session.query(cls).get(game_id)

    @classmethod
    def find_by_title(cls, session, title_query):
        """Finds games with titles containing the query string (case-insensitive)."""
        return session.query(cls).filter(cls._title.ilike(f"%{title_query}%")).all()

    def update(self, session, title=None, platform=None, genre=None, release_year=None, rating=None, developer=None, publisher=None):
        """Updates the game's attributes."""
        updated = False
        try:
            if title is not None:
                self.title = title; updated = True
            if platform is not None:
                if not isinstance(platform, Platform): raise TypeError("Invalid Platform object for update.")
                self.platform = platform; updated = True
            if genre is not None:
                if not isinstance(genre, Genre): raise TypeError("Invalid Genre object for update.")
                self.genre = genre; updated = True
            if release_year is not None or release_year == 0: # Allow setting to None/0 if that's intended
                self.release_year = release_year; updated = True
            if rating is not None or rating == 0: # Allow setting to None/0
                self.rating = rating; updated = True
            if developer is not None or developer == "REMOVE_DEV": # Special value to remove developer
                if developer == "REMOVE_DEV": self.developer = None
                elif not isinstance(developer, Developer): raise TypeError("Invalid Developer object for update.")
                else: self.developer = developer
                updated = True
            if publisher is not None or publisher == "REMOVE_PUB": # Special value to remove publisher
                if publisher == "REMOVE_PUB": self.publisher = None
                elif not isinstance(publisher, Publisher): raise TypeError("Invalid Publisher object for update.")
                else: self.publisher = publisher
                updated = True

            if updated:
                session.commit()
            return updated
        except (TypeError, ValueError) as e:
            session.rollback()
            print(f"Error updating game '{self.title}': {e}")
            return False
        except Exception as e:
            session.rollback()
            print(f"An unexpected error occurred during game update: {e}")
            return False


    def delete(self, session):
        """Deletes the game instance from the database."""
        try:
            session.delete(self)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error deleting game '{self.title}': {e}")
            return False

    def __repr__(self):
        platform_name = self.platform.name if self.platform else "N/A"
        genre_name = self.genre.name if self.genre else "N/A"
        return (
            f"<Game(id={self.id}, title='{self.title}', "
            f"platform='{platform_name}', genre='{genre_name}', year={self.release_year})>"
        )
