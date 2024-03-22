import pyodbc

# Connect to SQL Server
conn = pyodbc.connect('DRIVER={SQL SERVER};SERVER=BOOK-SQSVMSQG51\SQLEXPRESS;DATABASE=python_project;')
cursor = conn.cursor()

# Create Users table
cursor.execute("""
CREATE TABLE Users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    username VARCHAR(255) UNIQUE
)
""")

# Create Watchlist table
cursor.execute("""
CREATE TABLE Watchlist (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT,
    movie_name VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES Users(id)
)
""")

conn.commit()
conn.close()

print("Tables created successfully.")