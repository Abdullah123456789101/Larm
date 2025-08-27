import sqlite3

## Create a connection to the database
conn = sqlite3.connect('example.db')

## Create a cursor object to execute SQL statements
cursor = conn.cursor()

## Create a table called "users"
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    email TEXT
                )''')

## Insert sample data into the "users" table
users = [
    ('John Doe', 'johndoe@example.com'),
    ('Jane Smith', 'janesmith@example.com'),
    ('Bob Johnson', 'bobjohnson@example.com')
]
cursor.executemany('INSERT INTO users (name, email) VALUES (?, ?)', users)

## Commit the changes to the database
conn.commit()

## Close the cursor and the database connection
cursor.close()
conn.close()