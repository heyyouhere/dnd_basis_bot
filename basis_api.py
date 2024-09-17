from enum import Enum
#import requests_async
import requests
import urllib
import json
from random import randint

def get_random_class():
    roll = randint(1, 3)
    if roll == 1:
        return ClassType.TROOPER
    if roll == 2:
        return ClassType.SPY
    if roll == 3:
        return ClassType.HACKER

def get_random_race():
    roll = randint(1, 3)
    if roll == 1:
        return RaceType.HUMAN
    if roll == 2:
        return RaceType.ACTUR
    if roll == 3:
        return RaceType.HOBO

def __populate_collection():
    for i in range(0, 50):
        create_character(i, f"User_{i}", -1)
        set_race(i, get_random_race())
        set_class(i, get_random_class())
        set_mail(i, "spy@mail")
        set_phone(i, "+1234_spy")
        update_skill(i, SkillType.STR, randint(1, 30))
        update_skill(i, SkillType.AGL, randint(1, 30))
        update_skill(i, SkillType.WIS, randint(1, 30))
        event_completed(i, EventType.WHEEL)

base_url = "http://heyyouhere.space:1566/"
class RaceType(Enum):
    HUMAN = 1
    ACTUR = 2 
    HOBO = 3

class ClassType(Enum):
    TROOPER = 1
    SPY = 2
    HACKER = 3

class SkillType(Enum):
    STR = 1
    AGL = 2
    WIS = 3

class EventType(Enum):
    AR = 1
    WHEEL = 2
    QUEST = 3

def add_ar_points(effective_user_id, amount):
    payload = {
            "effective_user_id": effective_user_id,
            "points_amount": amount,
            }
    en = urllib.parse.urlencode(payload)
    res = requests.post(base_url + 'add_ar_points?' + en)

def create_character(effective_user_id, effective_user_username, chat_id):
    payload = {
            "effective_user_id": effective_user_id,
            "effective_user_username": effective_user_username,
            "chat_id": chat_id
            }
    en = urllib.parse.urlencode(payload)
    res = requests.post(base_url + 'create_character?' + en)

def set_race(effective_user_id, RaceType):
    payload = {
            "effective_user_id": effective_user_id,
            "character_race": RaceType.value
            }
    en = urllib.parse.urlencode(payload)
    res = requests.post(base_url + 'set_race?' + en)

def set_class(effective_user_id, ClassType):
    payload = {
            "effective_user_id": effective_user_id,
            "character_class": ClassType.value
            }
    en = urllib.parse.urlencode(payload)
    res = requests.post(base_url + 'set_class?' + en)

def update_skill(effective_user_id, SkillType, points):
    payload = {
            "effective_user_id": effective_user_id,
            "skill_id": SkillType.name,
            "points" : points
            }
    en = urllib.parse.urlencode(payload)
    res = requests.post(base_url + 'update_skill?' + en)

def event_completed(effective_user_id, EventType):
    payload = {
            "effective_user_id": effective_user_id,
            "event_type": EventType.name,
            }
    en = urllib.parse.urlencode(payload)
    res = requests.post(base_url + 'event_completed?' + en)

def spend_points(effective_user_id, amount_to_give_boss,  SkillType):
    payload = {
            "effective_user_id": effective_user_id,
            "points_amount" : amount_to_give_boss,
            "skill_id": SkillType.name,
            }
    en = urllib.parse.urlencode(payload)
    res = requests.post(base_url + 'spend_points?' + en)

def get_all_users_tg_id():
    res = requests.get(base_url + 'get_all_users_tg_id')
    return json.loads(res.content)

def get_top_users(amount=0):
    payload = {
            "amount" : amount,
            }
    en = urllib.parse.urlencode(payload)
    res = requests.get(base_url + 'get_leaders?' + en)
    return json.loads(res.content)

def get_character_data(effective_user_id):
    payload = {
            "effective_user_id": effective_user_id,
            }
    en = urllib.parse.urlencode(payload)
    res = requests.get(base_url + 'get_character_data?' + en)
    return json.loads(res.content)

def set_mail(effective_user_id, mail_str):
    payload = {
            "effective_user_id": effective_user_id,
            "mail" : mail_str,
            }
    en = urllib.parse.urlencode(payload)
    res = requests.post(base_url + 'set_mail?' + en)

def set_phone(effective_user_id, phone_str):
    payload = {
            "effective_user_id": effective_user_id,
            "phone" : phone_str,
            }
    en = urllib.parse.urlencode(payload)
    res = requests.post(base_url + 'set_phone?' + en)

if __name__ == '__main__':
    #create_character(1, f"vCore", -1)
    #create_character(2, f"DynamiX", -1)
    #create_character(3, f"Siberys", -1)
    #create_character(krops["tg_id"], krops['username'], krops['chat_id'])
    #update_skill(krops['tg_id'], SkillType.WIS, 6)


    exit(0)
    hyh_id = 249484136
    add_ar_points(hyh_id, 100)
    #set_phone(1, "hello, world")
    #get_top_hackers()
