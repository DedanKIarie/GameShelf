# GameShelf - Video Game Collection Tracker (CLI Edition)

GameShelf is a command-line interface (CLI) application designed to help users manage their personal video game collections. This project is built using Python and SQLAlchemy for Object-Relational Mapping (ORM).

## Project Goal

The primary goal of GameShelf is to provide a simple yet effective way to:
- Add new games to a collection with details (title, platform, genre, etc.).
- View the entire game collection.
- Filter and search for games.
- Update existing game information.
- Remove games from the collection.
- Manage related entities like platforms, genres, developers, and publishers.

## Core Technologies

- **Python 3.8+**
- **SQLAlchemy:** For ORM and database interaction (using SQLite).
- **Pipenv:** For managing project dependencies and virtual environment.
- **Standard Library:** For CLI interactions (no external CLI frameworks like Click).

## Directory Structure

```
gameshelf/
├── Pipfile
├── Pipfile.lock
├── README.md
└── lib/
    ├── __init__.py
    ├── models/
    │   ├── __init__.py     # Initializes models, Base, engine, Session
    │   ├── base.py         # Defines SQLAlchemy Base, engine, Session
    │   ├── platform.py     # Platform model
    │   ├── genre.py        # Genre model
    │   ├── developer.py    # Developer model
    │   ├── publisher.py    # Publisher model
    │   └── game.py         # Game model
    ├── db/
    │   ├── __init__.py
    │   └── seed.py         # Script to seed the database with sample data
    ├── cli.py              # Main CLI application logic (to be built)
    ├── helpers.py          # Helper functions for the CLI (to be built)
    └── debug.py            # Script for interactive debugging sessions (to be built)
```

## Getting Started

1.  **Clone the Repository:**
    ```bash
    # git clone <repository-url>
    # cd gameshelf
    ```
    (Or ensure you have the project files if not using Git yet)

2.  **Setup Environment and Install Dependencies:**
    Ensure you have Pipenv installed (`pip install pipenv`).
    ```bash
    pipenv install
    pipenv shell
    ```

3.  **Create Database and Seed Data (Optional but Recommended):**
    The database tables will be created automatically when the CLI application starts or when the seed script is run for the first time (via `lib.models.create_tables()`).
    To populate (or re-populate) the database with sample data:
    ```bash
    python -m lib.db.seed
    ```
    *(Note: The CLI will also have an option to run the seeder)*

4.  **Run the Application:**
    ```bash
    python lib/cli.py
    ```
    *(This will not do much yet as `cli.py` is not fully implemented)*

## Current Status (Commit 2)

- Basic project structure established.
- SQLAlchemy `Base`, `engine`, and `Session` configured in `lib/models/base.py`.
- All core models (`Platform`, `Genre`, `Developer`, `Publisher`, `Game`) defined in their respective files within `lib/models/`.
    - Each model includes:
        - Properties with validation (e.g., for `name`, `title`, `release_year`, `rating`).
        - Class methods for CRUD operations (e.g., `Model.create()`, `Model.get_all()`, `Model.find_by_id()`) and instance methods for update/delete.
        - Relationships defined (e.g., `Game` has one-to-many relationships with `Platform`, `Genre`, `Developer`, `Publisher`).
- `lib/models/__init__.py` updated to export all model components and the `create_tables()` function.
- Database seeding script `lib/db/seed.py` expanded to populate all models, including sample games with their relationships.
- This README file updated to reflect current progress.

Next steps will involve building the core CLI interaction logic in `lib/cli.py` and `lib/helpers.py`, and creating the `lib/debug.py` script.
```