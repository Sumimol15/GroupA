from flask import Flask, Response, request,jsonify
from datetime import datetime
import pyodbc
import json


app = Flask(__name__)


#
# Connect to the database
cnxn = pyodbc.connect(
    'Driver={SQL Server};'
    'Server=jerin.westeurope.cloudapp.azure.com;'
    'Database=ca1;'
    'UID=sa;'GET ALL USERS
@app.route('/getAllUsers')
def getAllUsers():    
    cursor = cnxn.cursor()    
    query = "  select userId,userName,firstName,lastName from users"    
    cursor.execute(query)
    rows = cursor.fetchall()
    column_names = [column[0] for column in cursor.description]
    row_dicts = []
    for row in rows:
        print(row)
        row_dict = dict(zip(column_names, row))        
        row_dicts.append(row_dict)

    # Close the cursor and database connection
    cursor.close()    
    return Response(json.dumps(row_dicts), mimetype='application/json')

#GET MY FRIENDS
@app.route('/getMyFriends', methods=['POST'])
def getMyFriends():  
    user_data = request.get_json()  
    cursor = cnxn.cursor()    
    query = "select distinct recipientId from messages where sentBy=?" 
    values = (user_data['userId'])   
    cursor.execute(query,values)
    rows = cursor.fetchall()
    friends=set()
    for row in rows:
       friends.add(row.recipientId)
    query = "select distinct sentBy from messages where recipientId=?" 
    values = (user_data['userId'])   
    cursor.execute(query,values)
    rows = cursor.fetchall()
    for row in rows:
       friends.add(row.sentBy)
    friendsString=""
    for element in friends:
        friendsString+=str(element)+','
    query = "  select userId,userName,firstName,lastName from users where userId in ("+friendsString[:len(friendsString)-1]+")" 
    print('SELECT QUERY FOR FINDING FRIENDS:'+query)   
    cursor.execute(query)
    rows = cursor.fetchall()
    column_names = [column[0] for column in cursor.description]
    row_dicts = []
    for row in rows:
        print(row)
        row_dict = dict(zip(column_names, row))        
        row_dicts.append(row_dict)
    cursor.close()    
    return Response(json.dumps(row_dicts), mimetype='application/json')
    'PWD=RandomPassword123;'
)


@app.route('/')
def home():
    return 'Hello, World!'


def checkForUserExist(emailId):
    cursor = cnxn.cursor()
    
    query = "SELECT count(*) FROM users where emailId=?"
    values=(emailId)
    cursor.execute(query,values)
    rows = cursor.fetchone()
    cursor.close()  
    
    if(rows[0]==0):return False
    else: return True
@app.route('/registerUser',  methods=['POST'])
def registerUser():
    user_data = request.get_json()
    # Create a cursor object to execute SQL queries
    print('chekcOne')
    if(checkForUserExist(user_data['emailId'])):
        response = {'message': 'User already exists'}
        return jsonify(response), 500
    cursor = cnxn.cursor()

    query = "INSERT INTO users VALUES (next VALUE for userSequence, ?, ?, ?, ?, ?,current_timestamp)"
    values = (user_data['emailId'], user_data['firstName'],user_data['lastName'],user_data['emailId'],user_data['password'])

    try:
        # Execute the INSERT statement
        cursor.execute(query, values)
        cnxn.commit()
        query = "select top 1 userId from users where userName=?"
        values = (user_data['emailId'])
        cursor.execute(query, values)
        row = cursor.fetchone()
        cursor.close()
        

        # Return a success response
        response = {'message': 'User created successfully','userId':row[0],'status':0}
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
#GET ALL USERS
@app.route('/getAllUsers')
def getAllUsers():    
    cursor = cnxn.cursor()    
    query = "  select userId,userName,firstName,lastName from users"    
    cursor.execute(query)
    rows = cursor.fetchall()
    column_names = [column[0] for column in cursor.description]
    row_dicts = []
    for row in rows:
        print(row)
        row_dict = dict(zip(column_names, row))        
        row_dicts.append(row_dict)

    # Close the cursor and database connection
    cursor.close()    
    return Response(json.dumps(row_dicts), mimetype='application/json')

#GET MY FRIENDS
@app.route('/getMyFriends', methods=['POST'])
def getMyFriends():  
    user_data = request.get_json()  
    cursor = cnxn.cursor()    
    query = "select distinct recipientId from messages where sentBy=?" 
    values = (user_data['userId'])   
    cursor.execute(query,values)
    rows = cursor.fetchall()
    friends=set()
    for row in rows:
       friends.add(row.recipientId)
    query = "select distinct sentBy from messages where recipientId=?" 
    values = (user_data['userId'])   
    cursor.execute(query,values)
    rows = cursor.fetchall()
    for row in rows:
       friends.add(row.sentBy)
    friendsString=""
    for element in friends:
        friendsString+=str(element)+','
    query = "  select userId,userName,firstName,lastName from users where userId in ("+friendsString[:len(friendsString)-1]+")" 
    print('SELECT QUERY FOR FINDING FRIENDS:'+query)   
    cursor.execute(query)
    rows = cursor.fetchall()
    column_names = [column[0] for column in cursor.description]
    row_dicts = []
    for row in rows:
        print(row)
        row_dict = dict(zip(column_names, row))        
        row_dicts.append(row_dict)
    cursor.close()    
    return Response(json.dumps(row_dicts), mimetype='application/json')
    
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
        
        return jsonify(response), 200

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


#API FOR MESSAGE CREATION
@app.route('/createMessage',  methods=['POST'])
def createMessage():
    user_data = request.get_json()
    # Create a cursor object to execute SQL queries
    cursor = cnxn.cursor()

    query = "INSERT INTO messages VALUES (next VALUE for messageSequence, ?, ?, ?, CURRENT_TIMESTAMP,'false')"
    values = (user_data['sentBy'], user_data['recipientId'],user_data['message'])

    try:
        # Execute the INSERT statement
        cursor.execute(query, values)
        cnxn.commit()
        query = "select top 1 messageId from messages where sentBy=? and recipientId=? and messageContent=? order by messageId desc"
        values = (user_data['sentBy'], user_data['recipientId'],user_data['message'])
        cursor.execute(query, values)
        row = cursor.fetchone()
        # Close the cursor 
        cursor.close()
        

        # Return a success response
        if(row):
            response = {'message': 'Message created successfully','status':0,'messageId':row[0]}
        return jsonify(response), 200

    except Exception as e:
        # Handle any errors that occur during the database operation
        # Rollback the transaction
        cnxn.rollback()

        # Close the cursor and database connection
        cursor.close()
        print(str(e))

        # Return an error response
        response = {'error': str(e)}
        return jsonify(response), 500
@app.route('/getMessages',methods=['POST'])
def message():
    user_data = request.get_json()
    # Create a cursor object to execute SQL queries
    cursor = cnxn.cursor()
    if(user_data['order'].lower()=='desc'):order='desc'
    else:order='asc'
    # Execute the SELECT statement
    query = "  select top "+str(user_data['noOfMessages'])+" * from messages where sentBy=? and recipientId=? order by messageId "+order
    values = (user_data['sentBy'], user_data['recipientId'])
    cursor.execute(query, values)

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

if __name__ == '__main__':
    app.run()