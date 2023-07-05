from flask import Flask
import pyodbc


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

