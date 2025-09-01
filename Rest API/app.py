from flask import Flask, jsonify, request
import sqlite3

# teste REST API med terminal:
# få alle users:
# curl.exe http://localhost:8080/users

# få en user med at erstatte <user_id> med nummer:
# curl.exe http://localhost:8080/users/<user_id>

# lave ny user:
# curl.exe -X POST -H "Content-Type: application/json" -d '{"name":"John Doe","email":"johndoe@example.com"}' http://localhost:8080/users

# updatere user:
# curl.exe -X PUT -H "Content-Type: application/json" -d '{"name":"Updated Name","email":"updated@example.com"}' http://localhost:8080/users/<user_id>

# fjerne user:
# curl.exe -X DELETE http://localhost:8080/users/<user_id>




## Create the Flask application
app = Flask(__name__)

## Endpoint to retrieve all users
@app.route('/users', methods=['GET'])
def get_users():
    ## Connect to the database
    conn = sqlite3.connect('Rest API/example.db')
    cursor = conn.cursor()

    ## Execute the SQL query to retrieve all users
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()

    ## Close the cursor and the database connection
    cursor.close()
    conn.close()

    ## Return the users as JSON
    return jsonify(users)


## Endpoint to retrieve a specific user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    ## Connect to the database
    conn = sqlite3.connect('Rest API/example.db')
    cursor = conn.cursor()

    ## Execute the SQL query to retrieve the user by ID
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()

    ## Close the cursor and the database connection
    cursor.close()
    conn.close()

    ## Check if the user exists
    if user:
        return jsonify(user)
    else:
        return jsonify({'message': 'User not found'}), 404


## Endpoint to create a new user
@app.route('/users', methods=['POST'])
def create_user():
    ## Get the user data from the request body
    data = request.get_json()
    name = data['name']
    email = data['email']

    ## Connect to the database
    conn = sqlite3.connect('Rest API/example.db')
    cursor = conn.cursor()

    ## Execute the SQL query to insert a new user
    cursor.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
    conn.commit()

    ## Close the cursor and the database connection
    cursor.close()
    conn.close()

    ## Return a success message
    return jsonify({'message': 'User created successfully'})


## Endpoint to update an existing user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    ## Get the updated user data from the request body
    data = request.get_json()
    name = data['name']
    email = data['email']

    ## Connect to the database
    conn = sqlite3.connect('Rest API/example.db')
    cursor = conn.cursor()

    ## Execute the SQL query to update the user
    cursor.execute('UPDATE users SET name = ?, email = ? WHERE id = ?', (name, email, user_id))
    conn.commit()

    ## Close the cursor and the database connection
    cursor.close()
    conn.close()

    ## Return a success message
    return jsonify({'message': 'User updated successfully'})


## Endpoint to delete a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    ## Connect to the database
    conn = sqlite3.connect('Rest API/example.db')
    cursor = conn.cursor()

    ## Execute the SQL query to delete the user
    cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()

    ## Close the cursor and the database connection
    cursor.close()
    conn.close()

    ## Return a success message
    return jsonify({'message': 'User deleted successfully'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)