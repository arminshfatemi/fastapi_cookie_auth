from pymongo import MongoClient

client = MongoClient()

database = client['test_db']

user_collection = database['user_collection']


def check_exist(username):
    if user_collection.find_one({'username': username}):
        return False
    else:
        return True