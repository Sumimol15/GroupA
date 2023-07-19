from flask import Flask, Response, request,jsonify,render_template
from datetime import datetime
import pyodbc
import json


app = Flask(__name__,template_folder='template')


#
# Connect to the database
cnxn = pyodbc.connect(
    #'Driver={ODBC Driver 18 for SQL Server};'  #FOr linux #Uncomment Based on the platforms, Thanks!
    'Driver={SQL Server};' # For Windows #Uncomment Based on the platforms, Thanks!
    'Server=jerin.westeurope.cloudapp.azure.com;' 
    'Database=ca1;'
    'UID=sa;'
    'PWD=RandomPassword123;'
    'TrustServerCertificate=yes;'
)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/message.html')
def messageHtml():
    return render_template('message.html')

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
        response = {'message': 'User already exists','status':2}
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
        response = {'error': str(e),'status':1}
        return jsonify(response), 500
#Login Logout
@app.route('/login',  methods=['POST'])
def login():
    user_data = request.get_json()
    # Create a cursor object to execute SQL queries
    cursor = cnxn.cursor()

    query = "SELECT password,userId,firstName FROM users WHERE userName=?"
    values = (user_data['userName'])

    try:
        # Execute the INSERT statement
        cursor.execute(query, values)
        row = cursor.fetchone()
        if row:
            print(row[0])
            if(row[0] == user_data['password']):
                response = {'message': 'Successfully Logged in','status':0,'userId':row[1],'firstName':row[2]}
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


#FETCH USER DETAILS
@app.route('/userDetails',  methods=['GET'])
def userDetails():
    userId = request.args['userId']
    cursor1 = cnxn.cursor()    
    query = "  select userId,userName,firstName,lastName from users where userId="+userId    
    cursor1.execute(query)
    row = cursor1.fetchone()
    column_names = [column[0] for column in cursor1.description]
    cursor1.close()    

      
    print(row)
    row_dict = dict(zip(column_names, row))        
   

    # Close the cursor and database connection
    return Response(json.dumps(row_dict), mimetype='application/json')



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
    query = "  select top "+str(user_data['noOfMessages'])+" * from messages where ((sentBy=? and recipientId=?) or (sentBy=? and recipientId=? )) order by messageId "+order
    values = (user_data['sentBy'], user_data['recipientId'], user_data['recipientId'],user_data['sentBy'])
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


#TOGGLE READ STATUS
def toggle(readStatus,sentBy,recipientId):
    cursor = cnxn.cursor()
    query = "UPDATE messages SET readStatus=? where sentBy=? and recipientId=?"
    values = (readStatus.lower(), sentBy,recipientId)
    try:
        # Execute the INSERT statement
        cursor.execute(query, values)
        cnxn.commit()
        query = "select readStatus from messages where sentBy=? and recipientId=? "
        values = (sentBy,recipientId)
        cursor.execute(query, values)
        row = cursor.fetchone()
        # Close the cursor 
        cursor.close()
        

        # Return a success response
        if(row):
            response = {'message': 'Conversation status updated successfully','status':0,'readStatus':row[0]}
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

@app.route('/readConversation',  methods=['POST'])
def readConversation():
    user_data = request.get_json()
    # Create a cursor object to execute SQL queries    
    readStatus=user_data['readStatus']
    if(type(user_data['readStatus'])==bool):
        if(user_data['readStatus']==True):readStatus="true"
        else:readStatus="false"   
    return toggle(readStatus,user_data['sentBy'],user_data['recipientId'])

    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080')