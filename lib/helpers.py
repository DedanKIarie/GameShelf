# lib/helpers.py
# Change this:
# from lib.models import Session, Platform, Genre, Developer, Publisher, Game
# To this:
import lib.models # Import the whole module

def exit_program():
    """Prints a goodbye message and exits the program."""
    print("Goodbye! Thanks for using GameShelf.")
    exit()

def get_string_input(prompt, min_len=1, max_len=100):
    """Gets a non-empty string input from the user with length validation."""
    while True:
        try:
            value = input(prompt).strip()
            if not value and min_len > 0: 
                print("Input cannot be empty.")
            elif not (min_len <= len(value) <= max_len):
                print(f"Input must be between {min_len} and {max_len} characters.")
            else:
                return value
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


def get_int_input(prompt, min_val=None, max_val=None, allow_empty=False):
    """Gets an integer input from the user, with optional range validation and allowance for empty input."""
    while True:
        try:
            value_str = input(prompt).strip()
            if allow_empty and not value_str:
                return None
            
            if not value_str and not allow_empty:
                print("Input cannot be empty. Please enter a number.")
                continue

            value = int(value_str)
            if min_val is not None and value < min_val:
                print(f"Value must be at least {min_val}.")
            elif max_val is not None and value > max_val:
                print(f"Value must be no more than {max_val}.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter a whole number.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


def display_platforms(session):
    """Displays all platforms."""
    platforms = lib.models.Platform.get_all(session) # Changed
    if not platforms:
        print("No platforms found.")
        return
    print("\n--- Platforms ---")
    for p in platforms:
        game_count = 0
        if hasattr(p, 'games') and p.games is not None: # Check if games attribute exists and is loaded
            game_count = len(p.games)
        print(f"ID: {p.id} | Name: {p.name} | Games: {game_count}")
    print("-----------------")

def display_genres(session):
    """Displays all genres."""
    genres = lib.models.Genre.get_all(session) # Changed
    if not genres:
        print("No genres found.")
        return
    print("\n--- Genres ---")
    for g in genres:
        game_count = 0
        if hasattr(g, 'games') and g.games is not None:
            game_count = len(g.games)
        print(f"ID: {g.id} | Name: {g.name} | Games: {game_count}")
    print("-----------------")

def display_developers(session):
    """Displays all developers."""
    developers = lib.models.Developer.get_all(session) # Changed
    if not developers:
        print("No developers found.")
        return
    print("\n--- Developers ---")
    for d in developers:
        game_count = 0
        if hasattr(d, 'games') and d.games is not None:
            game_count = len(d.games)
        print(f"ID: {d.id} | Name: {d.name} | Games: {game_count}")
    print("-----------------")

def display_publishers(session):
    """Displays all publishers."""
    publishers = lib.models.Publisher.get_all(session) # Changed
    if not publishers:
        print("No publishers found.")
        return
    print("\n--- Publishers ---")
    for p in publishers:
        game_count = 0
        if hasattr(p, 'games') and p.games is not None:
            game_count = len(p.games)
        print(f"ID: {p.id} | Name: {p.name} | Games: {game_count}")
    print("-----------------")

def display_games(session, games_list=None):
    """Displays a list of games. If no list is provided, displays all games."""
    if games_list is None:
        games_list = lib.models.Game.get_all(session) # Changed
    
    if not games_list:
        print("No games found matching your criteria.")
        return
    print("\n--- Games Collection ---")
    for game in games_list:
        platform_name = game.platform.name if game.platform else "N/A"
        genre_name = game.genre.name if game.genre else "N/A"
        dev_name = game.developer.name if game.developer else "N/A"
        pub_name = game.publisher.name if game.publisher else "N/A"
        year = game.release_year if game.release_year else "N/A"
        rating = game.rating if game.rating else "N/R"

        print(f"ID: {game.id} | Title: {game.title} ({year})")
        print(f"  Platform: {platform_name} | Genre: {genre_name} | Rating: {rating}/5")
        print(f"  Developer: {dev_name} | Publisher: {pub_name}")
        print("-" * 20)
    print("------------------------")

def select_model_instance(session, model_class, prompt_message="Select an item"):
    """
    Displays a list of instances for a given model and lets the user select one by ID.
    Returns the selected instance, or 'new' if the user wants to create one, or None.
    `model_class` is expected to be like `lib.models.Platform`.
    """
    instances = model_class.get_all(session) # model_class is already fully qualified
    if not instances:
        print(f"No {model_class.__name__}s found in the database.")
        create_new = input(f"Would you like to create a new {model_class.__name__}? (y/n): ").lower()
        if create_new == 'y':
            return "new"
        return None

    print(f"\nAvailable {model_class.__name__}s:")
    for instance in instances:
        print(f"  ID: {instance.id} - {instance.name}")

    while True:
        try:
            user_input = input(f"{prompt_message} (enter ID, or type 'new' to create one, 'skip' to leave empty): ").strip().lower()
            if user_input == 'new':
                return "new"
            if user_input == 'skip':
                return "skip"
            
            instance_id = int(user_input)
            selected_instance = model_class.find_by_id(session, instance_id) # model_class is already fully qualified
            if selected_instance:
                return selected_instance
            else:
                print("Invalid ID. Please choose from the list or type 'new'/'skip'.")
        except ValueError:
            print("Invalid input. Please enter a number for the ID, or type 'new'/'skip'.")
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
