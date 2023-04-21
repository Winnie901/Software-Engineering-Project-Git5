# from flask import Flask
from flask import Flask, render_template, request, redirect, url_for, session
import pymysql.cursors
import json
import pickle
from flask import jsonify
import sklearn
from flask_sqlalchemy import model

# Loading in the training models that we will be using later
bike_model = pickle.load(open('bikes_model.pkl', 'rb'))
stands_model = pickle.load(open('stands_model.pkl','rb'))


app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'dbbikes.cvvkn6jkfbdf.eu-west-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'SEGroup25'
app.config['MYSQL_PASSWORD'] = 'SEGroup25?'
app.config['MYSQL_DB'] = 'dbbikes'
app.config['MYSQL_PORT'] = 3306

# create a connection to the database
conn = pymysql.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    db=app.config['MYSQL_DB'],
    port=app.config['MYSQL_PORT'],
    cursorclass=pymysql.cursors.DictCursor

)

# Creating the route for the main page the user will access
@app.route('/')
def index():
    # cursor that will execute the SQL query to the database
    cursor = conn.cursor()
    
    # Selecting the last 117 entries from the availability table
    cursor.execute('SELECT * FROM availability ORDER BY last_update DESC LIMIT 117')
    availability_results = cursor.fetchall()

    # Selecting all the information from the stations table
    cursor.execute('SELECT * FROM stations')
    location_results = cursor.fetchall()
    
    # Debugging code print statements to make sure the query executed successfully
    print(availability_results)
    print(location_results)

    
    # Gathering station coordinate, name, and number values
    locations = []
    for location in location_results:
        latitude = location['position_lat']
        longitude = location['position_long']
        name = location['stat_name']
        number = location['number']
        
        # Gathering available bike values and available bike stand values
        bikes_available = None
        for availability in availability_results:
            if availability['number'] == location['number']:
                bikes_available = availability['available_bikes']
                bike_stands_available = availability['available_bike_stands']
                break
        
        # Adding each to the list locations
        locations.append((latitude, longitude, bikes_available, name, bike_stands_available,number))
    
    # Returning all information which will be used in conjunction with adding markers to a map and displaying window information
    return render_template('index.html', API_KEY='AIzaSyCmEmTVXz4FLSsTM3JME9J3VW-WXECqmKw', locations=locations)


# Route for when the user wants to route from one station to another
@app.route('/mapping.html')
def map():
    
    # Exact same code as the the previous route
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM availability ORDER BY last_update DESC LIMIT 117')

    availability_results = cursor.fetchall()

    # Getting the locations
    cursor.execute('SELECT * FROM stations')
    location_results = cursor.fetchall()
    print(availability_results)
    print(location_results)
    # extracting all the lat and long values
    locations = []
    for location in location_results:
        latitude = location['position_lat']
        longitude = location['position_long']
        name = location['stat_name']
        number = location['number']

        bikes_available = None
        for availability in availability_results:
            if availability['number'] == location['number']:
                bikes_available = availability['available_bikes']
                bike_stands_available = availability['available_bike_stands']
                break

        locations.append((latitude, longitude, bikes_available, name, bike_stands_available,number))

    return render_template('mapping.html', API_KEY='AIzaSyCmEmTVXz4FLSsTM3JME9J3VW-WXECqmKw', locations=locations)


# Route that will return the news portion of the site
@app.route('/news.html')
def news():
    return render_template('news.html')


# Route that will return the how-to portion of the site
@app.route('/how-to.html')
def howto():
    return render_template('how-to.html')

@app.route('/availability/<int:station_id>')
def predict_bikes(station_id):
    from datetime import datetime
    today = datetime.today()
    dow,month = today.weekday(),today.month

    predict_array = []
    json_dict = {}
    for h in range(24):
        predict_array.append([station_id,month,h,0,99,99,99,99,dow])
    results = bike_model.predict(predict_array).tolist()
    for index,bikes in enumerate(results):
        json_dict[index] = bikes

    return json.dumps(json_dict)

@app.route('/standsavailability/<int:stand_id>')
def predict_stands(stand_id):
    from datetime import datetime
    today = datetime.today()
    dow,month = today.weekday(),today.month

    predict_array = []
    json_dict = {}
    for h in range(24):
        predict_array.append([stand_id,month,h,0,99,99,99,99,dow])
    results = stands_model.predict(predict_array).tolist()
    for index,stands in enumerate(results):
        json_dict[index] = stands

    return json.dumps(json_dict)

# Start the application
if __name__ == "__main__":
    app.run(host ="0.0.0.0", port =8080, debug = True)
