# from flask import Flask
from flask import Flask, render_template, request, redirect, url_for, session
import pymysql.cursors
import json
import pickle
import jsonify
import sklearn
from flask_sqlalchemy import model

bike_model = pickle.load(open('bikes_model.pkl','rb'))
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

@app.route('/')
def index():
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM availability ORDER BY last_update DESC LIMIT 117')

    # I'm going to try and get the correct availability results

    # Fetch the results and close the connection
    availability_results = cursor.fetchall()

    # Getting the locations
    cursor.execute('SELECT * FROM stations')
    location_results = cursor.fetchall()
    print(availability_results)
    print(location_results)
    # Now we will be extracting all the lat and long values
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

    return render_template('index.html', API_KEY='AIzaSyCmEmTVXz4FLSsTM3JME9J3VW-WXECqmKw', locations=locations)



@app.route('/mapping.html')
def map():
    # Execute a SELECT query that will join available bikes and location
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM availability ORDER BY last_update DESC LIMIT 117')

    # I'm going to try and get the correct availability results

    # Fetch the results and close the connection
    availability_results = cursor.fetchall()

    # Getting the locations
    cursor.execute('SELECT * FROM stations')
    location_results = cursor.fetchall()
    print(availability_results)
    print(location_results)
    # Now we will be extracting all the lat and long values
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


@app.route('/news.html')
def news():
    return render_template('news.html')



@app.route('/how-to.html')
def howto():
    return render_template('how-to.html')

@app.route('/availability/<int:station_id>')
def predict_bikes(station_id):
    # ['number', 'month', 'hour', 'minute', 'weather_main', 'main_temp', 'main_humidity', 'wind_speed', 'dayofweek']
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
    # ['number', 'month', 'hour', 'minute', 'weather_main', 'main_temp', 'main_humidity', 'wind_speed', 'dayofweek']
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


if __name__ == "__main__":
    app.run(host ="0.0.0.0", port =5000, debug = True)