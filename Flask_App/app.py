from flask import Flask, jsonify, render_template
import mysql.connector

# Creating the Flask app

app = Flask(__name__, template_folder='templates')


# The following function will be used to setup the connection

def db_connection():
    connect = mysql.connector.connect(
        host='dbbikes.cvvkn6jkfbdf.eu-west-1.rds.amazonaws.com', # This is what was in the github repo
        port=3306,
        database='dbbikes',
        user='SEGroup25',
        password='SEGroup25?'
    )
    return connect


# Example route that uses the database connection
@app.route('/map')
def index():
    # Create a new database connection
    conn = db_connection()

    # Execute a SELECT query that will join available bikes and location
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM availability ORDER BY last_update DESC LIMIT 115')

    # I'm going to try and get the correct availability results








    # Fetch the results and close the connection
    availability_results = cursor.fetchall()
    

    # Getting the locations
    cursor.execute('SELECT * FROM stations')
    location_results = cursor.fetchall()

    # Now we will be extracting all the lat and long values
    locations = []
    for location in location_results:
        latitude = location[4]
        longitude = location[5]
        name = location[3]
        
        bikes_available = None
        for availability in availability_results:
            if availability[3] == location[0]:
                bikes_available = availability[1]
                bike_stands_available = availability[0]
                break
        

        
        locations.append((latitude, longitude, bikes_available, name, bike_stands_available))

    return render_template('map.html', API_KEY='AIzaSyCmEmTVXz4FLSsTM3JME9J3VW-WXECqmKw', locations=locations)




if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)