import dbinfo
import json
import requests
link = 'https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=5ac1b590c7e338d66c34fa0c5610e94c99a3b45c'
getStaticData = requests.get(link)
staticDataFile = getStaticData.json()
staticDataFile
print("£")