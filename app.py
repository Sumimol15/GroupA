from flask import Flask, Response
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
@app.route('/users')
def user():
    # Create a cursor object to execute SQL queries
    cursor = cnxn.cursor()

    # Execute the SELECT statement
    query = "SELECT * FROM users"
    cursor.execute(query)

    # Fetch all rows from the result set
    rows = cursor.fetchall()

    # Print the rows
    for row in rows:
        print(row)

    # Close the cursor and database connection
    cursor.close()    
    for row in rows:
        return(row.userName+row.firstName)
if __name__ == '__main__':
    app.run()