# lib/db/seed.py
from lib.models import Session, Platform, Genre, Developer, Publisher, Game
# from lib.models import create_tables # Already imported if run directly via __main__

def seed_database():
    session = Session()
    print("Seeding database...")

    # Clear existing data in reverse order of dependencies for safety
    # Game depends on others, so delete games first.
    # For a student project, they might skip this or do it less robustly.
    # A more robust way is to handle this with SQLAlchemy's cascade options or careful ordering.
    print("Clearing existing data (Games, then others)...")
    try:
        session.query(Game).delete()
        # Deleting related items like platforms/genres might fail if games still reference them
        # and cascade isn't set up. The model delete methods have checks.
        # For seeding, it's often simpler to delete all games, then all of the items they reference.
        # The individual delete methods in models have checks, so we'll rely on those if we were to call them.
        # Direct delete like this bypasses Python-level checks in model.delete().
        session.query(Platform).delete() # Simple clear for seeding
        session.query(Genre).delete()
        session.query(Developer).delete()
        session.query(Publisher).delete()
        session.commit()
        print("Cleared existing data from tables.")
    except Exception as e:
        session.rollback()
        print(f"Error clearing data: {e}. This might happen if there are existing relationships.")


    # Create Platforms
    platforms_data = ["PC", "PlayStation 5", "Nintendo Switch", "Xbox Series X", "Steam Deck"]
    created_platforms = {}
    for name in platforms_data:
        p = Platform.create(session, name=name)
        if p: created_platforms[name] = p

    # Create Genres
    genres_data = ["RPG", "Action", "Strategy", "Adventure", "Platformer", "Indie", "Simulation"]
    created_genres = {}
    for name in genres_data:
        g = Genre.create(session, name=name)
        if g: created_genres[name] = g

    # Create Developers
    developers_data = [
        "CD Projekt Red", "Nintendo EPD", "Santa Monica Studio",
        "FromSoftware", "Rockstar Games", "Larian Studios", "Valve"
    ]
    created_developers = {}
    for name in developers_data:
        d = Developer.create(session, name=name)
        if d: created_developers[name] = d

    # Create Publishers
    publishers_data = [
        "CD Projekt", "Nintendo", "Sony Interactive Entertainment",
        "Bandai Namco Entertainment", "Take-Two Interactive", "Larian Studios Publishing", "Valve"
    ]
    created_publishers = {}
    for name in publishers_data:
        pub = Publisher.create(session, name=name)
        if pub: created_publishers[name] = pub
    
    print(f"Seeded {len(created_platforms)} platforms, {len(created_genres)} genres, {len(created_developers)} developers, {len(created_publishers)} publishers.")

    # Create Games (using the created objects)
    games_to_seed = [
        {
            "title": "The Witcher 3: Wild Hunt", "release_year": 2015, "rating": 5,
            "platform_name": "PC", "genre_name": "RPG",
            "developer_name": "CD Projekt Red", "publisher_name": "CD Projekt"
        },
        {
            "title": "Cyberpunk 2077", "release_year": 2020, "rating": 4,
            "platform_name": "PC", "genre_name": "RPG",
            "developer_name": "CD Projekt Red", "publisher_name": "CD Projekt"
        },
        {
            "title": "The Legend of Zelda: Breath of the Wild", "release_year": 2017, "rating": 5,
            "platform_name": "Nintendo Switch", "genre_name": "Adventure",
            "developer_name": "Nintendo EPD", "publisher_name": "Nintendo"
        },
        {
            "title": "God of War Ragnarök", "release_year": 2022, "rating": 5,
            "platform_name": "PlayStation 5", "genre_name": "Action",
            "developer_name": "Santa Monica Studio", "publisher_name": "Sony Interactive Entertainment"
        },
        {
            "title": "Elden Ring", "release_year": 2022, "rating": 5,
            "platform_name": "PC", "genre_name": "RPG",
            "developer_name": "FromSoftware", "publisher_name": "Bandai Namco Entertainment"
        },
        {
            "title": "Baldur's Gate 3", "release_year": 2023, "rating": 5,
            "platform_name": "PC", "genre_name": "RPG",
            "developer_name": "Larian Studios", "publisher_name": "Larian Studios Publishing"
        },
        {
            "title": "Half-Life: Alyx", "release_year": 2020, "rating": 5,
            "platform_name": "PC", "genre_name": "Action", # Assuming PC VR
            "developer_name": "Valve", "publisher_name": "Valve"
        }
    ]

    games_added_count = 0
    for game_data in games_to_seed:
        # Retrieve the actual objects using the names (or handle if not found)
        platform_obj = created_platforms.get(game_data["platform_name"])
        genre_obj = created_genres.get(game_data["genre_name"])
        dev_obj = created_developers.get(game_data["developer_name"]) # Can be None
        pub_obj = created_publishers.get(game_data["publisher_name"]) # Can be None

        if platform_obj and genre_obj: # Required fields
            game = Game.create(
                session,
                title=game_data["title"],
                platform=platform_obj,
                genre=genre_obj,
                release_year=game_data.get("release_year"),
                rating=game_data.get("rating"),
                developer=dev_obj,
                publisher=pub_obj
            )
            if game:
                games_added_count +=1
                print(f"Created game: {game.title}")
            else:
                print(f"Failed to create game: {game_data['title']} (check logs for validation or other errors)")
        else:
            print(f"Skipping game '{game_data['title']}' due to missing platform or genre object during seeding.")
    
    print(f"Added {games_added_count} sample games.")
    session.close()
    print("Database seeding process complete.")

if __name__ == '__main__':
    from lib.models import create_tables
    create_tables() # Ensure tables exist
    seed_database()
