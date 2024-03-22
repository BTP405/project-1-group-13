import database

def prompt_add_user():
    username = input("Enter username: ")
    database.add_user(username)

def prompt_delete_user():
    username = input("Enter username to delete: ")
    database.delete_user(username)

def prompt_view_all_users():
    users = database.all_users()
    if users:
        print("All users:")
        for user in users:
            print(user[1])  # Assuming username is the second column in the database
    else:
        print("No users found.")

def prompt_search_movies():
    search_term = input("Enter movie title to search: ")
    movies = database.search_movies_api(search_term)
    if movies:
        print("Search results:")
        for movie in movies:
            print(f"{movie['title']} ({movie['release_date']})")
    else:
        print("No movies found.")

def prompt_add_movie_to_watchlist():
    username = input("Enter username: ")
    
    # Check if the user exists
    if not database.user_exists(username):
        print(f"User '{username}' does not exist. Cannot add movie to watchlist.")
        return

    movie_name = input("Enter movie name to add to watchlist: ")
    database.add_movie_to_watchlist(username, movie_name)

def prompt_remove_movie_from_watchlist():
    username = input("Enter username: ")
    
    # Check if the user exists
    if not database.user_exists(username):
        print(f"User '{username}' does not exist.")
        return

    movie_name = input("Enter movie name to remove from watchlist: ")
    
    # Check if the movie exists in the user's watchlist
    if not database.movie_exists_in_watchlist(username, movie_name):
        print(f"Movie '{movie_name}' is not in the watchlist.")
        return

    database.remove_movie_from_watchlist(username, movie_name)

def prompt_view_watchlist():
    username = input("Enter username to view watchlist: ")
    
    # Check if the user exists
    if not database.user_exists(username):
        print(f"User '{username}' does not exist. Cannot view watchlist.")
        return

    watchlist = database.get_watchlist(username)
    if watchlist:
        print(f"Watchlist for user '{username}':")
        for movie in watchlist:
            print(movie[0])  # Movie name is at index 0
    else:
        print(f"No movies found in watchlist for user '{username}'.")

def prompt_view_movie_details():
    search_term = input("Enter movie title to view details: ")
    movie_details = database.search_movies_api(search_term)
    if movie_details:
        movie = movie_details[0]  # Assuming we only show details for the first movie found
        print("Movie Details:")
        print(f"Title: {movie['original_title']}")
        print(f"Release Date: {movie['release_date']}")
        print(f"Adult-rated: {movie['adult']}")
        print(f"Rating: {movie['vote_average']}")
        print(f"Overview: {movie['overview']}")
    
    else:
        print("Movie not found.")

menu = """
Please select one of the following options:
1) Add new user
2) Delete a user
3) View all users
4) Search for a movie
5) View movie details
6) Add movie to watchlist
7) View watchlist
8) Remove movie from watchlist
0) Exit
"""

print("Welcome to the movie watchlist app!")

while True:
    print(menu)
    choice = input("Enter your choice: ")
    
    if choice == '1':
        prompt_add_user()
    elif choice == '2':
        prompt_delete_user()
    elif choice == '3':
        prompt_view_all_users()
    elif choice == '4':
        prompt_search_movies()
    elif choice == '5':
        prompt_view_movie_details()
    elif choice == '6':
        prompt_add_movie_to_watchlist()
    elif choice == '7':
        prompt_view_watchlist()
    elif choice == '8':
        prompt_remove_movie_from_watchlist()
    elif choice == '0':
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please try again.")
