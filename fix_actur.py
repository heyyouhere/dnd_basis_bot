from pymongo import MongoClient
from bson import json_util
import json

client = MongoClient("127.0.0.1", 27017)
db = client['testdb']

collections = []
#collections.append(db['testcollection'])
#collections.append(db['dayone_test'])

collections.append(db['dayone_prod1'])
collections.append(db['dayone_prod2'])

collections.append(db['daytwo_prod1'])
collections.append(db['daytwo_prod2'])


players=[]

def bson_to_json(data):
    return json.loads(json_util.dumps(data))


for collection in collections:
    print(collection)
    for user in collection.find({'chat_id': {"$ne" : -1}}):
        user.pop("_id")
        players.append(bson_to_json(user))


print(players, len(players))
with open('players_result.json', 'w') as f:
    json.dump(players, f)

