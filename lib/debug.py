# lib/debug.py
# This script is for interactive debugging sessions.
# You can import your models and session here to play around with data.

# To use:
# 1. Activate your pipenv shell: `pipenv shell`
# 2. Run this script: `python lib/debug.py`
# This will drop you into an ipdb session.

import ipdb # ipdb is listed in Pipfile's [dev-packages]

from lib.models import Session, Platform, Genre, Developer, Publisher, Game
from lib.models import create_tables

if __name__ == '__main__':
    # Ensure tables exist if you're going to interact with the DB
    create_tables()
    
    # Create a session to use in the debugger
    session = Session()

    print("Starting debug session...")
    print("Available variables in this session:")
    print("  session   - SQLAlchemy session instance")
    print("  Platform, Genre, Developer, Publisher, Game - Your model classes")
    print("Example usage in ipdb:")
    print("  platforms = session.query(Platform).all()")
    print("  ipdb> platforms[0].name")
    print("  new_genre = Genre.create(session, name='Test Genre')")
    print("  session.commit() # If create method doesn't commit itself")
    print("  exit    - to quit ipdb")
    
    # This will start the ipdb debugger session.
    # You can then interact with your models and the session.
    ipdb.set_trace()

    # Code here will run after you exit ipdb
    session.close()
    print("Debug session ended.")
