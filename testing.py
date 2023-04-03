import sqlalchemy as sqla
from sqlalchemy import create_engine
from sqlalchemy import create_engine, text
import traceback
import glob
import os
import pprint
from pprint import pprint
import json
import requests
import time
from IPython.display import display
import traceback
import datetime
import time



url = "dbbikes.cvvkn6jkfbdf.eu-west-1.rds.amazonaws.com"
port = "3306"
db = "dbbikes"
user = "SEGroup25"
password = "SEGroup25?"

engine = create_engine(f"mysql+pymysql://{user}:{password}@{url}:{port}/{db}", echo=True)


APIKEY = "5ac1b590c7e338d66c34fa0c5610e94c99a3b45c"
NAME = "Dublin"
STATIONS = "https://api.jcdecaux.com/vls/v1/stations"


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
        # break
    return


# availability_to_db(r.text)

def main():
    while True:
        try:
            now = datetime.datetime.now()
            r = requests.get(STATIONS, params={"apiKey": APIKEY, "contract": NAME})
            print(r, now)
            # write_to_file(r.text)
            availability_to_db(r.text)
            time.sleep(5 * 60)
        except:
            print(traceback.format_exc())
            if engine is None:
                return


if __name__ == "__main__":
    main()

import datetime


def write_to_file2(text):
    now = datetime.datetime.now()
    with open(f"data/weather_{now}".replace(" ", "_"), "w") as f:
        f.write(text)


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
    while True:
        try:
            r = requests.get(url)
            print(r)
            # write_to_file(r.text)
            weather_to_db(r.text)
            time.sleep(5 * 60)
        except:
            print(traceback.format_exc())
            if engine is None:
                return


# if __name__ == "__weather__main__":
weather_main()