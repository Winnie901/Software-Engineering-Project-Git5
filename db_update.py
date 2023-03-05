from sqlalchemy import create_engine
import json
import requests
import time
import datetime
import traceback

url = "dbbikes.cvvkn6jkfbdf.eu-west-1.rds.amazonaws.com"
port = "3306"
db = "dbbikes"
user = "SEGroup25"
password = "SEGroup25?"
APIKEY = "5ac1b590c7e338d66c34fa0c5610e94c99a3b45c"
NAME = "Dublin"
STATIONS = "https://api.jcdecaux.com/vls/v1/stations"

engine = create_engine(f"mysql+pymysql://{user}:{password}@{url}:{port}/{db}", echo=True)


def weather_to_db(text):
    weather = json.loads(text)
    print(type(weather), len(weather))
    print(text)
    now = datetime.datetime.now()
    vals = (
        now.strftime("%Y-%m-%d %H:%M:%S"),
        weather.get("coord").get("lon"),
        weather.get("coord").get("lat"),
        weather.get("weather")[0].get("main"),
        weather.get("main").get("temp"),
        weather.get("main").get("humidity"),
        weather.get("wind").get("speed"),
        weather.get("wind").get("deg"),
        datetime.datetime.utcfromtimestamp(weather.get("sys").get("sunset")).strftime('%Y-%m-%d %H:%M:%S'),
        datetime.datetime.utcfromtimestamp(weather.get("sys").get("sunrise")).strftime('%Y-%m-%d %H:%M:%S')
    )

    print("\n\n\nVALS:{}\n\n\n".format(vals))
    engine.execute("insert into weather values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", vals)


def weather_main():
    try:
        weather_url = "https://api.openweathermap.org/data/2.5/weather?q=Dublin,IE&units=metric&appid=3f8d6a1b1c08e87d9aa40e783517b136"
        r = requests.get(weather_url)
        weather_to_db(r.text)
    except:
        print(traceback.format_exc())
        if engine is None:
            return


def stations_to_db(text):
    stations = json.loads(text)
    print(type(stations), len(stations))
    print(text)

    for station in stations:
        print(station)
        vals = (
            station.get("number"),
            station.get("contract_name"),
            station.get("name"),
            station.get("address"),
            station.get("position").get("lat"),
            station.get("position").get("lng"),
            station.get("banking"),
            station.get("bonus"),
            station.get("bike_stands"),
            station.get("status")
        )
        print("\n\n\nVALS:{}\n\n\n".format(vals))
        engine.execute("insert into stations values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", vals)


def availability_to_db(text):
    availability = json.loads(text)
    print(type(availability), len(availability))
    for available in availability:
        print(available)
        vals = (
            (available.get("available_bike_stands")),
            (available.get("available_bikes")),
            available.get("last_update"),
            (available.get("number"))
        )
        engine.execute("insert into availability values(%s, %s, %s, %s)", vals)
    return


def stations_main():
    try:
        now = datetime.datetime.now()
        r = requests.get(STATIONS, params={"apiKey": APIKEY, "contract": NAME})
        print(r, now)
        #        stations_to_db(r.text)
        availability_to_db(r.text)
    except:
        print(traceback.format_exc())
        if engine is None:
            return


if __name__ == "__main__":
    stations_main()
    weather_main()
