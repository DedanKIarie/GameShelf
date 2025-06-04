# lib/cli.py

# Change this:
# from lib.models import Session, Platform, Genre, Developer, Publisher, Game, create_tables
# To this:
import lib.models # Import the whole module

# And keep these imports as they are (or adjust if they also face issues, but start with models)
from lib.db.seed import seed_database
from lib.helpers import (
    exit_program, get_string_input, get_int_input,
    display_platforms, display_genres, display_developers, display_publishers,
    display_games, select_model_instance
)

# IMPORTANT: You will also need to update how Platform, Genre, etc. are referenced
# in the functions like main_menu, games_menu, add_new_game, etc.
# For example, `Platform` will become `lib.models.Platform`.
# Let's apply this change systematically.

def main_menu(session):
    """Displays the main menu and handles user choices."""
    while True:
        print("\n--- GameShelf Main Menu ---")
        print("1. Manage Games")
        print("2. Manage Platforms")
        print("3. Manage Genres")
        print("4. Manage Developers")
        print("5. Manage Publishers")
        print("6. Seed Database (Warning: Clears existing data)")
        print("0. Exit Program")
        choice = input("> ")

        if choice == "1":
            games_menu(session)
        elif choice == "2":
            manage_simple_model_menu(session, lib.models.Platform, "Platform", display_platforms) # Changed
        elif choice == "3":
            manage_simple_model_menu(session, lib.models.Genre, "Genre", display_genres) # Changed
        elif choice == "4":
            manage_simple_model_menu(session, lib.models.Developer, "Developer", display_developers) # Changed
        elif choice == "5":
            manage_simple_model_menu(session, lib.models.Publisher, "Publisher", display_publishers) # Changed
        elif choice == "6":
            confirm_seed = input("This will clear ALL data and re-seed. Are you sure? (yes/no): ").lower()
            if confirm_seed == 'yes':
                print("Seeding database...")
                seed_database() 
                print("Database seeded.")
            else:
                print("Seeding cancelled.")
        elif choice == "0":
            exit_program()
        else:
            print("Invalid choice. Please try again.")

def games_menu(session):
    """Menu for managing games."""
    while True:
        print("\n--- Manage Games ---")
        print("1. List All Games")
        print("2. Add New Game")
        print("3. Find Game by ID")
        print("4. Find Games by Title")
        print("5. Update Game")
        print("6. Delete Game")
        print("0. Back to Main Menu")
        choice = input("> ")

        if choice == "1":
            display_games(session)
        elif choice == "2":
            add_new_game(session)
        elif choice == "3":
            find_game_by_id_action(session)
        elif choice == "4":
            find_games_by_title_action(session)
        elif choice == "5":
            update_game_action(session)
        elif choice == "6":
            delete_game_action(session)
        elif choice == "0":
            break
        else:
            print("Invalid choice.")

def add_new_game(session):
    """Handles adding a new game."""
    print("\n--- Add New Game ---")
    title = get_string_input("Enter game title: ", max_len=150)
    
    platform = select_or_create_related_model(session, lib.models.Platform, "Platform") # Changed
    if not platform: return

    genre = select_or_create_related_model(session, lib.models.Genre, "Genre") # Changed
    if not genre: return

    release_year = get_int_input("Enter release year (e.g., 2023) (optional, press Enter to skip): ", 1950, 2077, allow_empty=True)
    rating = get_int_input("Enter rating (1-5) (optional, press Enter to skip): ", 1, 5, allow_empty=True)

    developer = select_or_create_related_model(session, lib.models.Developer, "Developer", optional=True) # Changed
    if developer == "failed_create": return

    publisher = select_or_create_related_model(session, lib.models.Publisher, "Publisher", optional=True) # Changed
    if publisher == "failed_create": return

    game = lib.models.Game.create(session, title, platform, genre, release_year, rating, developer, publisher) # Changed
    if game:
        print(f"Success! Game '{game.title}' added with ID: {game.id}.")
    else:
        print("Failed to add game. Check previous error messages.")


def select_or_create_related_model(session, model_class, model_name, optional=False):
    """Helper to select an existing related model or create a new one."""
    # model_class is already passed as lib.models.ModelName, so no change needed inside this function
    while True:
        prompt_msg = f"Select {model_name}"
        if optional:
            prompt_msg += " (ID, 'new', or 'skip')"
        else:
            prompt_msg += " (ID or 'new')"

        selected = select_model_instance(session, model_class, prompt_msg) # select_model_instance needs to handle model_class correctly

        if selected == "skip" and optional:
            return None
        if selected == "new":
            new_name = get_string_input(f"Enter new {model_name} name: ")
            instance = model_class.create(session, name=new_name) # Uses model_class directly
            if instance:
                print(f"{model_name} '{instance.name}' created with ID {instance.id}.")
                return instance
            else:
                print(f"Failed to create {model_name}. Please try again or select an existing one.")
                if not optional: continue
                else: return "failed_create"
        elif selected:
            return selected
        elif not selected and not optional:
                 print(f"A {model_name} is required. Please select or create one.")
        elif not selected and optional:
                return None


def find_game_by_id_action(session):
    game_id = get_int_input("Enter Game ID to find: ")
    if game_id is not None:
        game = lib.models.Game.find_by_id(session, game_id) # Changed
        if game:
            display_games(session, [game])
        else:
            print(f"No game found with ID {game_id}.")

def find_games_by_title_action(session):
    search_term = get_string_input("Enter title (or part of title) to search for: ")
    games = lib.models.Game.find_by_title(session, search_term) # Changed
    if games:
        display_games(session, games)
    else:
        print(f"No games found with title containing '{search_term}'.")
            
def update_game_action(session):
    game_id = get_int_input("Enter ID of the game to update: ")
    game = lib.models.Game.find_by_id(session, game_id) # Changed
    if not game:
        print(f"Game with ID {game_id} not found.")
        return

    print(f"\nUpdating Game: {game.title} (ID: {game.id})")
    print("Leave input blank to keep current value.")

    new_title = input(f"New title (current: {game.title}): ").strip() or None
    
    print(f"\nCurrent Platform: {game.platform.name if game.platform else 'N/A'}")
    new_platform = select_or_create_related_model(session, lib.models.Platform, "Platform", optional=True) # Changed
    if new_platform == "failed_create": new_platform = game.platform
    elif new_platform == "skip": new_platform = game.platform
    
    print(f"\nCurrent Genre: {game.genre.name if game.genre else 'N/A'}")
    new_genre = select_or_create_related_model(session, lib.models.Genre, "Genre", optional=True) # Changed
    if new_genre == "failed_create": new_genre = game.genre
    elif new_genre == "skip": new_genre = game.genre

    new_year_str = input(f"New release year (current: {game.release_year or 'N/A'}): ").strip()
    new_year = game.release_year # Default to current
    if new_year_str == "": pass # Keep current if blank
    elif new_year_str.lower() == 'none' or new_year_str == '0': new_year = None
    else:
        try: new_year = int(new_year_str)
        except ValueError: print("Invalid year, keeping current.")


    new_rating_str = input(f"New rating (1-5) (current: {game.rating or 'N/A'}): ").strip()
    new_rating = game.rating # Default to current
    if new_rating_str == "": pass
    elif new_rating_str.lower() == 'none' or new_rating_str == '0': new_rating = None
    else:
        try: 
            new_rating_val = int(new_rating_str)
            if 1 <= new_rating_val <= 5: new_rating = new_rating_val
            else: print("Rating out of 1-5 range, keeping current.")
        except ValueError: print("Invalid rating, keeping current.")


    print(f"\nCurrent Developer: {game.developer.name if game.developer else 'N/A'}")
    new_developer = select_or_create_related_model(session, lib.models.Developer, "Developer", optional=True) # Changed
    if new_developer == "failed_create": new_developer = game.developer
    elif new_developer == "skip": new_developer = game.developer


    print(f"\nCurrent Publisher: {game.publisher.name if game.publisher else 'N/A'}")
    new_publisher = select_or_create_related_model(session, lib.models.Publisher, "Publisher", optional=True) # Changed
    if new_publisher == "failed_create": new_publisher = game.publisher
    elif new_publisher == "skip": new_publisher = game.publisher
    
    update_args = {}
    if new_title is not None and new_title != game.title : update_args['title'] = new_title
    # Ensure new_platform, new_genre etc. are the actual objects or None
    if not isinstance(new_platform, str): # Avoid passing "failed_create" or "skip"
        if new_platform != game.platform : update_args['platform'] = new_platform
    if not isinstance(new_genre, str):
        if new_genre != game.genre : update_args['genre'] = new_genre
    if new_year != game.release_year : update_args['release_year'] = new_year
    if new_rating != game.rating : update_args['rating'] = new_rating
    if not isinstance(new_developer, str):
      if new_developer != game.developer : update_args['developer'] = new_developer
    if not isinstance(new_publisher, str):
      if new_publisher != game.publisher : update_args['publisher'] = new_publisher


    if not update_args:
        print("No changes made.")
        return

    if game.update(session, **update_args):
        print(f"Game '{game.title}' (ID: {game.id}) updated successfully.")
    else:
        print(f"Failed to update game '{game.title}'. Check validation errors.")


def delete_game_action(session):
    game_id = get_int_input("Enter ID of the game to delete: ")
    game = lib.models.Game.find_by_id(session, game_id) # Changed
    if not game:
        print(f"Game with ID {game_id} not found.")
        return
    
    confirm = input(f"Are you sure you want to delete '{game.title}' (ID: {game.id})? (yes/no): ").lower()
    if confirm == 'yes':
        if game.delete(session):
            print(f"Game '{game.title}' deleted successfully.")
        else:
            print(f"Failed to delete game '{game.title}'.")
    else:
        print("Deletion cancelled.")


def manage_simple_model_menu(session, model_class, model_name, display_func):
    # model_class is already lib.models.ModelName
    while True:
        print(f"\n--- Manage {model_name}s ---")
        print(f"1. List All {model_name}s")
        print(f"2. Add New {model_name}")
        print(f"3. Find {model_name} by ID")
        print(f"5. Update {model_name}")
        print(f"6. Delete {model_name}")
        print("0. Back to Main Menu")
        choice = input("> ")

        if choice == "1":
            display_func(session) # display_func needs to use lib.models if it queries directly
        elif choice == "2":
            name = get_string_input(f"Enter new {model_name} name: ")
            instance = model_class.create(session, name=name) # Uses model_class.create
            if instance:
                print(f"{model_name} '{instance.name}' added with ID: {instance.id}.")
            else:
                print(f"Failed to add {model_name}. It might already exist or name is invalid.")
        elif choice == "3":
            item_id = get_int_input(f"Enter {model_name} ID to find: ")
            if item_id is not None:
                instance = model_class.find_by_id(session, item_id) # Uses model_class.find_by_id
                if instance:
                    # Assuming instance.games exists for these simple models
                    game_count = 0
                    if hasattr(instance, 'games') and instance.games is not None:
                        game_count = len(instance.games)
                    print(f"Found: ID: {instance.id} | Name: {instance.name} | Games: {game_count}")
                else:
                    print(f"No {model_name} found with ID {item_id}.")
        elif choice == "5": 
            item_id = get_int_input(f"Enter ID of the {model_name} to update: ")
            instance = model_class.find_by_id(session, item_id) # Uses model_class.find_by_id
            if instance:
                new_name = get_string_input(f"Enter new name for '{instance.name}': ")
                if instance.update(session, name=new_name):
                    print(f"{model_name} updated to '{instance.name}'.")
                else:
                    print(f"Failed to update {model_name}. Name might be invalid or already in use.")
            else:
                print(f"{model_name} with ID {item_id} not found.")
        elif choice == "6": 
            item_id = get_int_input(f"Enter ID of the {model_name} to delete: ")
            instance = model_class.find_by_id(session, item_id) # Uses model_class.find_by_id
            if instance:
                confirm = input(f"Are you sure you want to delete '{instance.name}' (ID: {instance.id})? This cannot be undone. (yes/no): ").lower()
                if confirm == 'yes':
                    if instance.delete(session): 
                        print(f"{model_name} '{instance.name}' deleted.")
                    else:
                        print(f"Could not delete {model_name} '{instance.name}'. Check if it's associated with games.")
                else:
                    print("Deletion cancelled.")
            else:
                print(f"{model_name} with ID {item_id} not found.")
        elif choice == "0":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    print("Initializing GameShelf...")
    try:
        # Now call create_tables as an attribute of the imported lib.models module
        print("DEBUG: About to call lib.models.create_tables()")
        lib.models.create_tables() 
        print("DEBUG: lib.models.create_tables() called.")
        
        # And Session as an attribute
        db_session = lib.models.Session() 
        print("Welcome to GameShelf!")
        main_menu(db_session)
    except AttributeError as e:
        print(f"DEBUG: AttributeError during startup: {e}")
        print("This likely means a name (like create_tables or Session) was not found in lib.models.")
    except Exception as e:
        print(f"An error occurred during application startup: {e}")
        print("Please ensure your database is configured correctly.")
    finally:
        if 'db_session' in locals() and db_session: # type: ignore
            db_session.close() # type: ignore
            print("Database session closed.")
