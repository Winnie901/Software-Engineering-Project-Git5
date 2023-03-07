from flask import Flask, render_template, request, redirect, url_for, session
import requests

# You can add DB credentials here
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# This should be set equal to mysql://user:password@<your link>/<db name> to connect to aws instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://SEGROUP25:SEGROUP25?@dbbikes.cvvkn6jkfbdf.eu-west-1.rds.amazonaws.com/Dbbikes'

db = SQLAlchemy(app)

# You want a class that can represent this so its easier to deal with the data when trying to use it
class BikesData(db.Model):
    #    {
    #     "number": 42,
    #     "contract_name": "dublin",
    #     "name": "SMITHFIELD NORTH",
    #     "address": "Smithfield North",
    #     "position": {
    #         "lat": 53.349562,
    #         "lng": -6.278198
    #     },
    #     "banking": false,
    #     "bonus": false,
    #     "bike_stands": 30,
    #     "available_bike_stands": 0,
    #     "available_bikes": 30,
    #     "status": "OPEN",
    #     "last_update": 1677804020000
    # },
    number = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    contract_name = db.Column(db.String(80))
    name = db.Column(db.String(80))
    address = db.Column(db.String(80))
    lat = db.Column(db.String(80))
    lng = db.Column(db.String(80))
    banking = db.Column(db.String(80))
    bonus = db.Column(db.String(80))
    bike_stands = db.Column(db.String(80))
    available_bike_stands = db.Column(db.String(80))
    available_bikes = db.Column(db.String(80))
    status = db.Column(db.String(80))
    last_update = db.Column(db.String(80))


def get_bikes_from_api():
    # This gets the data from the api
    response = requests.get(
        "https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=00c8d74cfb42063ed62f296bc16d431b06ce879e")
    # this converts it to json and im returning it
    val = response.json()

    return val


def get_bikes_from_db():
    #  This will look something like this
    bikes = BikesData.query.all()
    return bikes


def get_available_bikes_from_db():
    #  This will look something like this
    bikes = BikesData.query()
    return bikes

def pick_up_bike():
    pass
    # update where number = 5

@app.route("/")
def home():
    # store the json im returning in a variable here

    bikes = get_bikes_from_api()

    # render the html template and pass in the bikes json which looks like a list of jsons
    # [
    # {
    #     "number": 42,
    #     "contract_name": "dublin",
    #     "name": "SMITHFIELD NORTH",
    #     "address": "Smithfield North",
    #     "position": {
    #         "lat": 53.349562,
    #         "lng": -6.278198
    #     },
    #     "banking": false,
    #     "bonus": false,
    #     "bike_stands": 30,
    #     "available_bike_stands": 0,
    #     "available_bikes": 30,
    #     "status": "OPEN",
    #     "last_update": 1677804020000
    # },
    # ...
    # ]

    # go to index.html file now
    return render_template('index.html', bikes=bikes)

@app.route('/claimBike')
def claimBike():
    pass


@app.route("/weather", methods=["POST", "GET"])
def weather():
    # I got the api key from signing up openweathermap.org
    # If form filled has city entry call api and redirect to display page else go to form again
    if request.form.get("city") is not None:
        api_key = "77f00c4957cf9aec8201dc8c6181157d"
        city_name = request.form.get("city")

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&appid={api_key}"
        # get method of requests module
        # return response object
        response = requests.get(url)

        # json method of response object
        # convert json format data into
        # python format data
        x = response.json()
        # Redirect to view page and pass in the json that we have scraped for weather
        return redirect(url_for('weather_view', test=x))
    else:
        return render_template("weather.html")


#  This page will be used to display weather after
@app.route("/weather_view")
def weather_view():
    import json
    #  Again city will be used in the weather_view.html page
    # The request.args['weather_json'] is not in dict format here
    # Converting it means changing single quotes to double and then using json.loads

    s = request.args['test'].replace("\'", "\"")

    return render_template("weather_view.html", city=json.loads(s))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)



# Here we are getting information from the DB in order to plot markers of
# the stations on our map

@app.route("/stations")
@functools.lru_cache(maxsize=128)
def get_stations():
    engine = get_db()
    sql = "select * from station ;"
    try:
        with engine.connect() as conn:
        rows = conn.execute(text(sql)).fetchall()
        print('#found {} stations', len(rows), rows)
        return jsonify([row._asdict() for row in rows])
    except:
        print(traceback.format_exc())
        return "error in get_stations", 404