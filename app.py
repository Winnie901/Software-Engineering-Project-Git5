from flask import Flask, render_template, request, redirect, url_for, session
import requests
import pymysql
# You can add DB credentials here
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db_params = {
    'host': 'localhost', # I think this needs to be changed to the full filepath of the aws location
    'port': 3306,
    'user': 'SEGroup25',
    'password': 'SEGroup25?',
    'database': 'dbbikes',
    'charset': 'utf8mb4'
}

# Build the MySQL connection URL
db_url = f"mysql://{db_params['SEGroup25']}:{db_params['SEGroup25?']}@{db_params['3306']}:{db_params['3306']}/{db_params['localhost']}?charset={db_params['utf8mb4']}"

# Create a MySQL connection pool
pool = pymysql.create_pool(host=db_params['localhost'], port=db_params['3306'], user=db_params['SEGroup25'], password=db_params['SEGroup25?'], db=db_params['localhost'], charset=db_params['utf8mb4'])

@app.route('/map') # This has been changed as we are specifying the 'map.html' file in our folder
def index():
    # Get a connection from the pool
    conn = pool.connection()
    cursor = conn.cursor()

    # Execute a SELECT query
    cursor.execute("SELECT * FROM mytable")
    
    # My version of executing the SELECT query
    # cursor.execute('SELECT * FROM availability ORDER BY last_update DESC LIMIT 115')
    # This should return the last 115 entries into the database, which should be the most
    # up to date availability numbers for the bikes

    

    # Fetch the results and store them in a list
    rows = cursor.fetchall()
    
    
    # I then grabbed the location values for all the rows in the station table, in order to plot
    # the markers
    
    # Getting the locations
    # cursor.execute('SELECT * FROM station')
    # location_results = cursor.fetchall()

    # Now we will be extracting all the lat and long values
    # locations = []
    # for location in location_results:
        # latitude = location[7]
        # longitude = location[8]
        # name = location[5]
        
        # bikes_available = None
        # for availability in availability_results:
            # if availability[0] == location[6]:
                # bikes_available = availability[1]
                # break
        

        
        # locations.append((latitude, longitude, bikes_available, name))

    # return render_template('map.html', API_KEY='AIzaSyCmEmTVXz4FLSsTM3JME9J3VW-WXECqmKw', locations=locations)
    
    
    
    
    

    # Close the connection
    conn.close()

    # Render the results in a template
    return render_template('index.html', rows=rows)

if __name__ == '__main__':
    app.run(debug=True)









# This should be set equal to mysql://user:password@<your link>/<db name> to connect to aws instance
#app.config['SQLALCHEMY_DATABASE_URI'] = 'pymysql://SEGROUP25:SEGROUP25?@dbbikes.cvvkn6jkfbdf.eu-west-1.rds.amazonaws.com/Dbbikes'

db = SQLAlchemy(app)

# Here we are getting information from the DB in order to plot markers of
# the stations on our map

# @app.route("/stations")
# @functools.lru_cache(maxsize=128)
# def get_stations():
#     engine = get_db()
#     sql = "select * from stations ;"
#     try:
#         with engine.connect() as conn:
#             rows = conn.execute(text(sql)).fetchall()
#         print('#found {} stations', len(rows), rows)
#         return jsonify([row._asdict() for row in rows])
#     except:
#         print(traceback.format_exc())
#         return "error in get_stations", 404



