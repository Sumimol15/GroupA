from flask import Flask, Response, request,jsonify
from datetime import datetime
import pyodbc
import json


app = Flask(__name__)


#
# Connect to the database
cnxn = pyodbc.connect(
    'Driver={SQL Server};'
    'Server=jerindatabase.database.windows.net;'
    'Database=sqldatabase;'
    'UID=jerin;'
    'PWD=RandomPassword123;'
)


@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/messages')
def message():
    # Create a cursor object to execute SQL queries
    cursor = cnxn.cursor()

    # Execute the SELECT statement
    query = "SELECT * FROM messages"
    cursor.execute(query)

    # Fetch all rows from the result set
    rows = cursor.fetchall()

    column_names = [column[0] for column in cursor.description]
    row_dicts = []
    for row in rows:
        print(row)
        row_dict = dict(zip(column_names, row))
        # Convert datetime objects to strings
        for key, value in row_dict.items():
            if isinstance(value, datetime):
                row_dict[key] = value.strftime('%Y-%m-%dT%H:%M:%S')
        row_dicts.append(row_dict)

    # Close the cursor and database connection
    cursor.close()    
    return Response(json.dumps(row_dicts), mimetype='application/json')
@app.route('/registerUser',  methods=['POST'])
def registerUser():
    user_data = request.get_json()
    # Create a cursor object to execute SQL queries
    cursor = cnxn.cursor()

    query = "INSERT INTO users VALUES (next VALUE for userSequence, ?, ?, ?, ?, ?,current_timestamp)"
    values = (user_data['emailId'], user_data['firstName'],user_data['lastName'],user_data['emailId'],user_data['password'])

    try:
        # Execute the INSERT statement
        cursor.execute(query, values)
        cnxn.commit()

        # Close the cursor 
        cursor.close()
        

        # Return a success response
        response = {'message': 'User created successfully'}
        return jsonify(response), 201

    except Exception as e:
        # Handle any errors that occur during the database operation
        # Rollback the transaction
        cnxn.rollback()

        # Close the cursor and database connection
        cursor.close()
        

        # Return an error response
        response = {'error': str(e)}
        return jsonify(response), 500
#Login Logout
@app.route('/login',  methods=['POST'])
def login():
    user_data = request.get_json()
    # Create a cursor object to execute SQL queries
    cursor = cnxn.cursor()

    query = "SELECT password FROM users WHERE userName=?"
    values = (user_data['userName'])

    try:
        # Execute the INSERT statement
        cursor.execute(query, values)
        row = cursor.fetchone()
        if row:
            print(row[0])
            if(row[0] == user_data['password']):
                response = {'message': 'Successfully Logged in','status':0}
            else:
                response = {'message': 'Login failed','status':1}
        else:
            response = {'message': 'User doesnot exist','status':2}
        # Close the cursor 
        cursor.close()
        

        # Return a success response
        
        return jsonify(response), 201

    except Exception as e:
        # Handle any errors that occur during the database operation
        # Rollback the transaction
        cnxn.rollback()

        # Close the cursor and database connection
        cursor.close()
        cnxn.close()

        # Return an error response
        response = {'error': str(e)}
        return jsonify(response), 500

if __name__ == '__main__':
    app.run()