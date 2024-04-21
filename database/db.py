from pymongo import MongoClient
from handle_password.security import *

client = MongoClient("mongodb://localhost:27017/")
db = client["FastAPI"]
users_collection = db["users"]


def authenticate_user(username: str, password: str):
    user = users_collection.find_one({"username": username})
    if not user:
        return False
    if not pwd_context.verify(password, user["password"]):
        return False
    return user


def create_user(user_data: dict):
    user_data["password"] = get_password_hash(user_data["password"])
    result = users_collection.insert_one(user_data)
    return result.inserted_id

def get_user(username: str):
    user = users_collection.find_one({"username": username})
    return user

def update_user(username: str, user_data: dict):
    updated_user = users_collection.update_one({"username": username}, {"$set": user_data})
    return updated_user.modified_count

def delete_user(username: str):
    result = users_collection.delete_one({"username": username})
    return result.deleted_count

