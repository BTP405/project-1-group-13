# Movie Watchlist App

## 1. Installation

### Dependencies
- Python 3.x
- pymongo (Python MongoDB driver)

### Installation Instructions
1. Clone the repository to your local machine.
2. Install the required dependencies using pip:
    ```
    pip install pymongo
    ```
3. Ensure you have MongoDB installed and running on your machine or provide the appropriate MongoDB connection URI.

## 2. Usage

### Rules
1. User has to exist to add movie to watch list
2. To add movie to watchlist, movie should exist in movies collection
   
### Examples
- To run the application, execute `app.py` using Python:
    ```
    python app.py
    ```

### Configuration
- Edit `database.py` to configure the MongoDB connection URI if necessary.

## 3. Features

- Add new movies to the watchlist.
- View all available movies.
- Mark movies as watched and manage watched movies.
- Add and delete users.
- Search for movies by title.

## 4. Contributing

### Guidelines
- Bug reports, feature requests, and contributions are welcome.
- Please submit any bugs or feature requests through the issue tracker.

### Code Style
- Follow PEP 8 guidelines for Python code.

## 5. Credits

### Authors
- Nand Patel, Rahman Mohamed, Amitoj Uppal

## 6. License

- This project is licensed under the MIT License - see the [LICENSE](https://en.wikipedia.org/wiki/MIT_License) file for details.
