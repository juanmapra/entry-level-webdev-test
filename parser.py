from dataclasses import dataclass
from typing import List
import json
from datetime import datetime
from pymongo import MongoClient

@dataclass
class UserPreferences:
    timezone: str

@dataclass
class User:
    username: str
    password: str
    roles: List[str]
    preferences: UserPreferences
    created_ts: float
    active: bool = True

client = MongoClient('localhost', 27017)
db = client['local']
collection = db['users']

with open('udata.json') as json_file:
    original_data = json.load(json_file)

parsed_users = []

for user_data in original_data['users']:
    roles = []
    if user_data['is_user_admin']:
        roles.append('admin')
    if user_data['is_user_manager']:
        roles.append('manager')
    if user_data['is_user_tester']:
        roles.append('tester')

    user_preferences = UserPreferences(timezone=user_data['user_timezone'])

    created_ts = datetime.strptime(user_data['created_at'], '%Y-%m-%dT%H:%M:%SZ').timestamp()

    parsed_user = User(
        username=user_data['user'],
        password=user_data['password'],
        roles=roles,
        preferences=user_preferences,
        active=user_data['is_user_active'],
        created_ts=created_ts
    )

    parsed_users.append(parsed_user)

for user in parsed_users:
    user_document = {
        "username": user.username,
        "password": user.password,
        "roles": user.roles,
        "preferences":{
            "timezone": user.preferences.timezone
        },
        "active": user.active,
        "created_ts": user.created_ts
    }
    collection.insert_one(user_document)

print("Data inserted successfully!")

for document in collection.find():
    print(document)