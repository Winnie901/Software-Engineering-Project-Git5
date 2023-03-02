# importing the required libraries
import requests
# Enter the api key of openweathermap here
api_key = "3f8d6a1b1c08e87d9aa40e783517b136"
# Base url for the open map api
root_url = "http://maps.openweathermap.org/maps/2.0/weather"
# City name for which we need the weather data
city_name = "dublin"
# Building the final url for the API call
url = f"{root_url}appid={api_key}&q={city_name}"
# sending a get request at the url
r = requests.get(url)
# displaying the json weather data returned by the api
print(r.json())