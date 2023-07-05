from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://jerin:RandomPassword123@jerindatabase.database.windows.net/sqldatabase?driver=ODBC+Driver+17+for+SQL+Server'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'jerindatabase.database.windows.net'  # Replace with your database URI
db = SQLAlchemy(app)

# Define a model for your table
class Test(db.Model):
    __tablename__ = 'test'
    test = db.Column(db.String, primary_key=False)
    # username = db.Column(db.String(50), unique=True)

@app.route('/')
def index():
    # Execute the select query
    users = Test.query.all()

    # Process the query results
    user_list = [user.username for user in users]

    # Return the results as a response
    return ', '.join(user_list)

if __name__ == '__main__':
    app.run()
