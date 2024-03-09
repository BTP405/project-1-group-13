import datetime
import pymongo

# Connect to MongoDB
try:
    client = pymongo.MongoClient("mongodb+srv://auppal12:TE7Y1AooYAZlYnHz@cluster1.nu3veit.mongodb.net/sample_airbnb?retryWrites=true&w=majority")
    db = client["movie_database"]
    movies_collection = db["movies"]
    users_collection = db["users"]
    watched_collection = db["watched"]
except pymongo.errors.ConnectionError as e:
    print(f"Error connecting to MongoDB: {e}")
    exit(1)

#MOVIE MANAGEMENT

def add_movie(title, release_timestamp):
    # Check if a movie with the same title already exists
    existing_movie = movies_collection.find_one({"title": title})

    if existing_movie:
        # Movie with the same title already exists
        print(f"Failed to add movie. Movie with the title '{title}' already exists.")
        return False

    # If the movie doesn't exist, add it to the movies collection
    try:
        movie_data = {"title": title, "release_timestamp": release_timestamp}
        movies_collection.insert_one(movie_data)
        print("New movie added.")
        return True
    except pymongo.errors.PyMongoError as e:
        print(f"Error adding movie to database: {e}")
        return False

def get_movies(upcoming=False):
    if upcoming:
        today_timestamp = datetime.datetime.today().timestamp()
        movies = movies_collection.find({"release_timestamp": {"$gt": today_timestamp}})
    else:
        movies = movies_collection.find()
    return list(movies)

def search_movies(search_term):
    regex_pattern = f".*{search_term}.*"
    result = movies_collection.find({"title": {"$regex": regex_pattern, "$options": "i"}})
    return list(result)


#USER MANAGEMENT
def add_user(username):
    # Check if the user already exists
    existing_user = users_collection.find_one({"username": username})

    if existing_user:
        # User already exists
        print(f"Failed to add user '{username}'. Username may already exist.\n")
        return False

    # If the user doesn't exist, add them to the users collection
    try:
        user_data = {"username": username}
        users_collection.insert_one(user_data)
        print(f"User '{username}' added.\n")
        return True
    except pymongo.errors.PyMongoError as e:
        print(f"Error adding user to database: {e}")
        return False

def delete_user(username):
    # Find and delete user from the users collection
    user_deleted = users_collection.delete_one({"username": username})

    if user_deleted.deleted_count == 0:
        # User not found
        print(f"User {username} not found.")
        return False

    # Delete watched movies associated with the user from the watched collection
    watched_collection.delete_many({"user_username": username})
    print(f"User {username} deleted.")
    return True

def all_users():
    user_count = users_collection.count_documents({})

    if user_count == 0:
        return "no user"

    return users_collection.find()

#WATCH LIST MANAGEMENT
def watch_movie(username, movie_name):
    # Check if the user exists
    existing_user = users_collection.find_one({"username": username})

    if not existing_user:
        print(f"User '{username}' does not exist. Cannot add watched movie.")
        return False

    # Check if the movie exists in the movies collection
    existing_movie = movies_collection.find_one({"title": movie_name})

    if not existing_movie:
        print(f"Movie '{movie_name}' does not exist in the movies collection. Cannot add to watchlist.")
        return False

    # Check if the movie is already in the watched collection for the user
    existing_watched_movie = watched_collection.find_one({"user_username": username, "movie_name": movie_name})

    if existing_watched_movie:
        print(f"Movie '{movie_name}' already exists in the watchlist for user '{username}'.")
        return False

    # If the user exists, the movie exists, and the movie doesn't exist in the watchlist, add the movie to the watched collection
    watched_data = {"user_username": username, "movie_name": movie_name}
    watched_collection.insert_one(watched_data)
    print(f"Movie '{movie_name}' added to the watchlist for user '{username}'.")
    return True


def get_watched_movies(username):
    pipeline = [
        {"$match": {"user_username": username}},
        {"$lookup": {
            "from": "movies",
            "localField": "movie_name",  # Update to the correct field name in watched_collection
            "foreignField": "title",    # Assuming the movie titles match the watched movies
            "as": "movie"
        }},
        {"$unwind": "$movie"},
        {"$project": {"_id": "$movie._id", "title": "$movie.title", "release_timestamp": "$movie.release_timestamp"}}
    ]
    return list(watched_collection.aggregate(pipeline))

def unwatch_movie(username, movie_name):
    # Find and delete the watched movie
    result = watched_collection.delete_one({"user_username": username, "movie_name": movie_name})
    
    if result.deleted_count > 0:
        print(f"Movie '{movie_name}' removed from the watchlist for user '{username}'.")
        return True
    else:
        print(f"Movie '{movie_name}' not found in the watchlist for user '{username}'.")
        return False