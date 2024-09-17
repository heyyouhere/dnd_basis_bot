from pymongo import MongoClient
from bson import json_util
import json

client = MongoClient("127.0.0.1", 27017)
db = client['testdb']
#collection = db['testcollection']
#collection = db['dayone_test']
#collection = db['dayone_prod1']
#collection = db['dayone_prod2']
collection = db['daytwo_prod1']



#collection.delete_many({})

def bson_to_json(data):
    return jsonify(json.loads(json_util.dumps(data)))

def print_collection():
    for doc in collection.find():
        print(doc)

print_collection()

from flask import Flask, jsonify, request, send_from_directory
app = Flask(__name__)

#import logging
#log = logging.getLogger('werkzeug')
#log.setLevel(logging.ERROR)


BOSS_STATS = {
        "STR" : 1,
        "AGL" : 1,
        "WIS" : 1,
    }

'''
player: {
     tg_id            : int,
     tg_username      : str,
     chat_id          : int,
     user_mail        : str,
     user_number      : str,
     character_race   : int,
     character_class  : int,
     skills: {
         "STR" : int,
         "AGL" : int,
         "WIS" : int
     },
     total_skill_points: int,
     activities_finished: {
        "AR"    : bool,
        "WHEEL" : bool,
        "QUEST" : bool,
     }
}
'''

@app.route('/')
def serve_leaderboard():
    return send_from_directory('./','leaderboard.html')

@app.route('/<path:path>')
def send_report(path):
    return send_from_directory('./', path)

@app.route('/create_character', methods=['POST'])
def create_user():
    tg_id = int(request.args.get('effective_user_id'))
    username = request.args.get('effective_user_username')
    chat_id = int(request.args.get('chat_id'))
    result = collection.find_one({"tg_id": tg_id})
    print(result)
    if result is None:
        collection.insert_one(
                {
                 "tg_id"               : tg_id,
                 "chat_id"             : chat_id,
                 "user_email"          : "",
                 "user_phone"          : "",
                 "username"            : username,
                 "character_race"      : 0,
                 "character_class"     : 0,
                 "total_skill_points"  : 0,
                 "skills" : {
                        "STR" : 1,
                        "AGL" : 1,
                        "WIS" : 1
                     },
                 "ar_points" : 0,
                 "activities_finished": {
                        "AR"   : False,
                        "WHEEL": False,
                        "QUEST": False,
                },
            })
        return 'OK', 200
    else:
        collection.update_one({"tg_id": tg_id}, 
                              {"$set": 
                                {"activities_finished" : {
                                        "AR"   : False,
                                        "WHEEL": False,
                                        "QUEST": False,}
                                 }
                               })
        collection.update_one({"tg_id": tg_id}, 
                              {"$set": 
                                {"skills" : {
                                        "STR" : 1,
                                        "AGL" : 1,
                                        "WIS" : 1,}
                                 }
                               })
        collection.update_one({"tg_id": tg_id}, [{"$set": {"total_skill_points": 3}}])
        collection.update_one({"tg_id": tg_id}, [{"$set": {"ar_points": 0}}])

    return 'ERROR', 500



def check_mongo_injection(input_str):
    forbidden_chars = ['$', '\\', '\0', '[', ']', '{', '}', '(', ')', '!', '"', "'"]
    for ch in forbidden_chars:
        input_str = input_str.replace(ch, "")
    return input_str


@app.route('/set_mail', methods=['POST'])
def set_mail():
    tg_id = int(request.args.get('effective_user_id'))
    mail = request.args.get('mail')
    mail = check_mongo_injection(mail)
    res = collection.update_one({"tg_id" : tg_id}, {'$set' :  {"user_email" : mail}})
    if res.modified_count == 1:
        return 'OK', 200
    return 'ERROR', 500

@app.route('/set_phone', methods=['POST'])
def set_phone():
    tg_id = int(request.args.get('effective_user_id'))
    phone = request.args.get('phone')
    phone = check_mongo_injection(phone)
    res = collection.update_one({"tg_id" : tg_id}, {'$set' :  {"user_phone" : phone}})
    if res.modified_count == 1:
        return 'OK', 200
    return 'ERROR', 500


@app.route('/set_race', methods=['POST'])
def set_race():
    tg_id = int(request.args.get('effective_user_id'))
    char_race = int(request.args.get('character_race'))
    res = collection.update_one({"tg_id" : tg_id}, {'$set' :  {"character_race" : char_race}})
    if res.modified_count == 1:
        return 'OK', 200
    return 'ERROR', 500


@app.route('/set_class', methods=['POST'])
def set_class():
    tg_id = int(request.args.get('effective_user_id'))
    char_class = int(request.args.get('character_class'))
    res = collection.update_one({"tg_id" : tg_id}, {'$set' :  {"character_class" : char_class}})
    if char_class == 1:
        collection.update_one({"tg_id" : tg_id}, {'$inc' : {f"skills.STR" : 1}})
    if char_class == 2:
        collection.update_one({"tg_id" : tg_id}, {'$inc' : {f"skills.AGL" : 1}})
    if char_class == 3:
        collection.update_one({"tg_id" : tg_id}, {'$inc' : {f"skills.WIS" : 1}})
    collection.update_one({"tg_id": tg_id}, [{"$set": {"total_skill_points": {"$sum": ["$skills.STR", "$skills.AGL", "$skills.WIS"]}}}])
    if res.modified_count == 1:
        return 'OK', 200
    return 'ERROR', 500


@app.route('/update_skill', methods=['POST'])
def update_skill():
    tg_id = int(request.args.get('effective_user_id'))
    skill_id = request.args.get('skill_id')
    points = int(request.args.get('points'))
    res = collection.update_one({"tg_id" : tg_id}, {'$inc' : {f"skills.{skill_id}" : points}})
    
    collection.update_one({"tg_id": tg_id}, [{"$set": {"total_skill_points": {"$sum": ["$skills.STR", "$skills.AGL", "$skills.WIS", "$ar_points"]}
        }}]
)
    if res.modified_count == 1:
        return 'OK', 200
    return 'ERROR', 500


@app.route('/event_completed', methods=['POST'])
def event_completed():
    tg_id = int(request.args.get('effective_user_id'))
    event_type = request.args.get('event_type')
    res = collection.update_one({"tg_id" : tg_id}, {'$set' : {f"activities_finished.{event_type}" : True}})
    if res.modified_count == 1:
        return 'OK', 200
    return 'ERROR', 500


@app.route('/get_character_data', methods=['GET'])
def get_character_data():
    tg_id = int(request.args.get('effective_user_id'))
    data = collection.find_one({"tg_id" : tg_id})
    return bson_to_json(data)

@app.route('/get_all_users_tg_id', methods=['GET'])
def get_all_users_tg_id():
    data = collection.find({}, {"tg_id":1, "username" : 1, "chat_id" : 1, "_id":0})
    return bson_to_json(data)


@app.route('/spend_points', methods=['POST'])
def spend_points():
    global BOSS_STATS
    tg_id = int(request.args.get('effective_user_id'))
    res = collection.update_one({"tg_id": tg_id}, {"$set": {"total_skill_points": 0}})

    points_amount = float(request.args.get('points_amount'))
    boss_skill_id = request.args.get('skill_id')
    BOSS_STATS[boss_skill_id] += points_amount

    if res.modified_count == 1:
        return 'OK', 200
    return 'ERROR', 500

@app.route('/add_ar_points', methods=['POST'])
def add_ar_points():
    tg_id = int(request.args.get('effective_user_id'))
    points_amount = int(request.args.get('points_amount'))
    collection.update_one({"tg_id": tg_id}, {"$inc": {"ar_points": points_amount}})
    res = collection.update_one({"tg_id": tg_id}, {"$inc": {"total_skill_points":  points_amount}})
    if res.modified_count == 1:
        return 'OK', 200
    return 'ERROR', 500

@app.route('/get_leaders', methods=['GET'])
def get_leaders():
    leaders_limit = request.args.get('amount')
    if leaders_limit:
        top_players = collection.find().sort("total_skill_points", -1).limit(int(leaders_limit))
    else:
        top_players = collection.find().sort("total_skill_points", -1)
    return bson_to_json(list(top_players))



@app.route('/get_boss_stats', methods=['GET'])
def get_boss_stats():
    global BOSS_STATS
    return jsonify(BOSS_STATS)

app.run(host='0.0.0.0', port=1566)
