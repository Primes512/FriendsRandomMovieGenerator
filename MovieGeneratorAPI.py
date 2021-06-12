# Cruz Lopez
# PSID: 1443590
# April 3, 2021
# Final Project - Sprint1
# CIS 3368

import flask
from flask import jsonify
from flask import request, make_response
import mysql.connector
from mysql.connector import Error
import random

# setting up an application name
app = flask.Flask(__name__) #set up application
app.config["DEBUG"] = True #allow to show error message in browser

@app.route('/', methods=['GET'])  #routing = mapping urls to functions; home is usually mapped to '/'
def home():
    return "<h1>Hi and welcome to Cruz's first API!</h1>"

@app.route('/friend', methods=['POST']) #set up friend page 
def addFriend():
    request_data = request.get_json()  
    firstName = request_data['firstName'] #getting user first name data
    lastName = request_data['lastName'] # getting user last name data
    conn = create_connection("cis3368.cdmfwx1asfpw.us-east-2.rds.amazonaws.com", "admin", "CLcis3368", "cis3368db") # database login
    query = "INSERT INTO friend (firstName, lastName) VALUES ('"+firstName+"','"+lastName+"')" #sql script
    execute_query(conn, query)  # executing connection to database
    return 'POST REQUEST WORKED'
    #check my table in mySQL Workbench to verify the user has been added

@app.route('/movieList', methods=['POST']) # set up movie list page
def addMovieList():
    request_data = request.get_json()
    newfriendID = request_data['friendID']  # getting friendID data
    newMovie1 = request_data['movie1'] #getting friends top ten movies from 1st movie to the tenth movie
    newMovie2 = request_data['movie2']
    newMovie3 = request_data['movie3']
    newMovie4 = request_data['movie4']
    newMovie5 = request_data['movie5']
    newMovie6 = request_data['movie6']
    newMovie7 = request_data['movie7']
    newMovie8 = request_data['movie8']
    newMovie9 = request_data['movie9']
    newMovie10 = request_data['movie10']
    conn = create_connection("cis3368.cdmfwx1asfpw.us-east-2.rds.amazonaws.com", "admin", "CLcis3368", "cis3368db")
    query = 'INSERT INTO movieList (friendID, movie1, movie2, movie3, movie4, movie5, movie6, movie7, movie8, movie9, movie10) VALUES (%s,"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'%(newfriendID, newMovie1, newMovie2, newMovie3, newMovie4, newMovie5, newMovie6, newMovie7, newMovie8, newMovie9, newMovie10) # Adding friend data into table
    execute_query(conn, query)  
    return 'POST REQUEST WORKED'
    #check my table in mySQL Workbench to verify the user has been added

@app.route('/decision', methods=['GET']) # set up decision page
def decision():
    if 'friendID' in request.args:
        id = int(request.args['friendID']) # getting user friendID argument input
    else: 
        return "ERROR: No id provided"
    
    conn = create_connection("cis3368.cdmfwx1asfpw.us-east-2.rds.amazonaws.com", "admin", "CLcis3368", "cis3368db")
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT movie1, movie2, movie3, movie4, movie5, movie6, movie7, movie8, movie9, movie10 FROM movieList WHERE friendID = %s"%(id)
    cursor.execute(sql)
    row = cursor.fetchone()
    return random.choice(list(row.values())) # getting random value from movielist


@app.route('/friend/allFriends', methods=['GET'])
def allFriends():
    conn = create_connection("cis3368.cdmfwx1asfpw.us-east-2.rds.amazonaws.com", "admin", "CLcis3368", "cis3368db")
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT * FROM friend"
    cursor.execute(sql)
    rows = cursor.fetchall()

    return jsonify(rows)

    # for user in rows:
    #     friend = user
    #     return friend

def create_connection(host_name, user_name, user_password, db_name):    # creating connection with database 
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

app.run() # running the app
