from flask import Flask
from flask import Flask, render_template, request, redirect, url_for, session
import pymysql.cursors

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
    conn.ping()  # reconnecting mysql
    with conn.cursor() as cursor:
        # execute a query
        cursor.execute('SELECT * FROM stations')

        # fetch the data
        stations_data = cursor.fetchall()

        # close the cursor and connection
        cursor.close()
    print(str(stations_data))
    location = []
    for row in stations_data:
        location.append((row['position_lat'],row['position_long']))

    print(location)
    # return the data to the user
    return render_template('index.html', locations=location)



@app.route('/mapping.html')
def map():

    conn.ping()  # reconnecting mysql
    with conn.cursor() as cursor:
        # execute a query
        cursor.execute('SELECT position_lat,position_long FROM stations')

        # fetch the data
        stations_data = cursor.fetchall()

        # close the cursor and connection
        cursor.close()
    print(str(stations_data))
    location = []
    for row in stations_data:
        location.append((row['position_lat'],row['position_long']))

    print(location)
    # return the data to the user
    return render_template('mapping.html', locations=location)


@app.route('/news.html')
def news():
    return render_template('news.html')

if __name__ == "__main__":
    app.run()