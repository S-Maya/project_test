from pymongo import MongoClient
import googlemaps
import json
import pandas as pd
from pprint import pprint
import config
client = MongoClient('mongodb://localhost:27017')
db = client.pymongo_test
df = pd.read_excel("brew_list2.xlsx")
brewery_list = df["name"]
gmaps = googlemaps.Client(key=config.apikey)
for brewery in brewery_list:
    try:
        result = gmaps.find_place(brewery, 'textquery')
        #print(result.status_code)
        place_id = result["candidates"][0]["place_id"]
        data = gmaps.place(place_id)
        posts = db.posts
        post_data = {
            'name': brewery,
            'address': data["result"]["formatted_address"] if data["result"]["formatted_address"] else "None",
            'phone': data["result"]["formatted_phone_number"] if data["result"]["formatted_phone_number"] else "None",
            'latitude': data["result"]["geometry"]["location"]["lat"] if data["result"]["geometry"]["location"]["lat"] else "None",
            'longitude' : data["result"]["geometry"]["location"]["lng"] if data["result"]["geometry"]["location"]["lng"] else "None"
        }
        result = posts.insert_one(post_data)
        print('One post: {0}'.format(result.inserted_id))
    except Exception as e:
        pass
