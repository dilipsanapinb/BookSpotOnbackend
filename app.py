from flask import Flask,request
from flask_mysqldb import MySQL
from dotenv import load_dotenv

import bcrypt
import jwt
app=Flask(__name__)
load_dotenv()

import os 
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']="Dilip@0123"
app.config['MYSQL_DB']='BookSpotOn'
mysql=MySQL(app)

@app.route('/')
def helloUser():
    return 'Welcome to the BooSpotOn: The leading booking app'

# # create new user
@app.route('/api/user', methods=['POST'])
def create_user():
    try:
        user_data = request.json
        username = user_data['username']
        email = user_data['email']
        password = user_data['password']
        role = user_data['role']
        membership = user_data['membership']

        hashed_password=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user (username, email, password, role, membership) VALUES (%s, %s, %s, %s, %s)", (username, email, hashed_password, role, membership))
        mysql.connection.commit()
        cur.close()

        return 'User created successfully'
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return 'Internal Server Error', 500


# login route

@app.route('/api/login',methods=['POST'])
def login():
    try:
        login_data=request.json
        username=login_data['username']
        password=login_data['password']
        cur=mysql.connection.cursor()
        cur.execute("SELECT id, username,password FROM user WHERE username=%s",(username,))
        user=cur.fetchone()
        cur.close()

        if user:
            stored_password=user[2].encoded('utf-8')
            if bcrypt.checkpw(password.ecode('utf-8'),stored_password):

                # to generate the json web token

            
                token=jwt.encode({'user_id':user[0]},os.getenv("SECRETE_KEY"),algorithm='HS256')
                return {'token':token.decode('utf-8')}
            return 'Invalid username or password'


    except Exception as e:
        print(f"An error occurred:{str(e)}")
        return 'Internal Server Error',500


# verify token function

def verify_token(token):
    try:
        decoded_token=jwt.decode(token,os.getenv("SECRETE_KEY"),algorithms=['HS256'])
        return decoded_token['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


# Example protected route
# @app.route('/api/protected', methods=['GET'])
# def protected():
#     try:
#         token = request.headers.get('Authorization')
#         if token:
#             user_id = verify_token(token)
#             if user_id:
#                 # User is authenticated, proceed with the protected resource
#                 return 'This is a protected resource'
#         return 'Unauthorized', 401
#     except Exception as e:
#         print(f"An error occurred: {str(e)}")
#         return 'Internal Server Error', 500
# # get a list of all users
# @app.route('/api/users',methods=['GET'])

# # get a user by id
# @app.route('/api/users/:id',methods=['GET'])

# # update a specific user info
# @app.route('/api/users/:id',methods=['PUT'])

# # delete a specific user
# @app.route('/api/users/:id',methods=['DELETE'])

# # Movies Routes
# #create a new movie
# @app.route('/api/movies',methods=['POST'])

# # get a list of all movies
# @app.route('/api/movies',methods=['GET'])

# # get a movie by id
# @app.route('/api/movies/:id',methods=['GET'])

# # update a movie by id 
# @app.route('/api/movies/:id',methods=['PUT'])

# # delete a movie by id 
# @app.route('/api/movies/:id',methods=['DELETE'])


# # theaters Routes
# #create a new movie
# @app.route('/api/theaters',methods=['POST'])

# # get a list of all theaters
# @app.route('/api/theaters',methods=['GET'])

# # get a movie by id
# @app.route('/api/theaters/:id',methods=['GET'])

# # update a movie by id 
# @app.route('/api/theaters/:id',methods=['PUT'])

# # delete a movie by id 
# @app.route('/api/theaters/:id',methods=['DELETE'])

# # show Routes
# #create a new movie
# @app.route('/api/show',methods=['POST'])

# # get a list of all show
# @app.route('/api/show',methods=['GET'])

# # get a movie by id
# @app.route('/api/show/:id',methods=['GET'])

# # update a movie by id 
# @app.route('/api/show/:id',methods=['PUT'])

# # delete a movie by id 
# @app.route('/api/show/:id',methods=['DELETE'])

# # events Routes
# #create a new movie
# @app.route('/api/events',methods=['POST'])

# # get a list of all events
# @app.route('/api/events',methods=['GET'])

# # get a movie by id
# @app.route('/api/events/:id',methods=['GET'])

# # update a movie by id 
# @app.route('/api/events/:id',methods=['PUT'])

# # delete a movie by id 
# @app.route('/api/events/:id',methods=['DELETE'])

# # participants Routes
# #create a new movie
# @app.route('/api/participants',methods=['POST'])

# # get a list of all participants
# @app.route('/api/participants',methods=['GET'])

# # get a movie by id
# @app.route('/api/participants/:id',methods=['GET'])

# # update a movie by id 
# @app.route('/api/participants/:id',methods=['PUT'])

# # delete a movie by id 
# @app.route('/api/participants/:id',methods=['DELETE'])

# # bookings Routes
# #create a new movie
# @app.route('/api/bookings',methods=['POST'])

# # get a list of all bookings
# @app.route('/api/bookings',methods=['GET'])

# # get a movie by id
# @app.route('/api/bookings/:id',methods=['GET'])

# # update a movie by id 
# @app.route('/api/bookings/:id',methods=['PUT'])

# # delete a movie by id 
# @app.route('/api/bookings/:id',methods=['DELETE'])

if __name__== '__main__':
    app.run()
    app.debug(True)
    

