import database
import datetime

def prompt_add_movie():
    title = input("Movie title: ")
    release_date = input("Release date (dd-mm-YYYY): ")

    try:
        parsed_date = datetime.datetime.strptime(release_date, "%d-%m-%Y")
        timestamp = parsed_date.timestamp()
        database.add_movie(title, timestamp)

    except ValueError:
        print("Invalid date format. Please enter the date in dd-mm-YYYY format.")

    print("\n")


def prompt_watch_movie():
    username = input("Username: ")
    movie_name = input("Enter movie name you've watched: ")
    database.watch_movie(username, movie_name)
    
    print("\n")

def prompt_remove_watched_movie():
    username = input("Username: ")
    watched_movie = input("Enter the movie name you want to remove from watched list: ")
    database.unwatch_movie(username, watched_movie)
    print("\n")


def print_movie_list(movies):
    if not movies:
        print(f"No movie found.\n")
        return

    for movie in movies:
        movie_date = datetime.datetime.fromtimestamp(movie["release_timestamp"])
        human_date = movie_date.strftime("%d %b %Y")
        print(f"{movie['title']} ({human_date})")
    
    print("\n")

def prompt_show_watched_movies():
    username = input("Username: ")
    movies = database.get_watched_movies(username)
    print_movie_list(movies)
    print("\n")


def prompt_search_movies():
    search_term = input("Enter movie title: ")
    movies = database.search_movies(search_term)
    return movies


def prompt_add_user():
    username = input("Username: ")
    database.add_user(username)

def prompt_delete_user():
    username = input("Username: ")
    database.delete_user(username)        
    print("\n")


def prompt_all_users():
    users = database.all_users()

    if isinstance(users, str) and users == "no user":
        print("No users found.")
    else:
        print("---All users in database---")
        for user in users:
            print(user["username"])
    
    print("\n")


menu = """Please select one of the following options:
0) Exit.
1) Add new movie.
2) View all movies.
3) Add watched movie.
4) View watched movies.
5) Remove watched movie.
6) Add new user.
7) Delete a user.
8) View all users.
9) Search for a movie.

Your selection: """
welcome = "Welcome to the watchlist app!"


print(welcome)

while (user_input := input(menu)) != "0":
    if user_input == "1":
        prompt_add_movie()
    elif user_input == "2":
        movies = database.get_movies(upcoming=False)
        print_movie_list(movies)
    elif user_input == "3":
        prompt_watch_movie()
    elif user_input == "4":
        prompt_show_watched_movies()
        print("\n")
    elif user_input == "5":
        prompt_remove_watched_movie()
    elif user_input == "6":
        prompt_add_user()
    elif user_input == "7":
        prompt_delete_user()
    elif user_input == "8":
        prompt_all_users()
    elif user_input == "9":
        movies = prompt_search_movies()
        if movies:
            print_movie_list(movies)
        else:
            print("Found no movies for that search term!\n")
    else:
        print("Invalid input, please try again!\n")