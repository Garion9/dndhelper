import pymongo.errors

from User_Module import *

try:
    register_user("dewkong123", "nie Dewkong", "nie dewkong321")
except pymongo.errors.DuplicateKeyError as err:
    print("User with chosen username already exists.")
    print("Exact error: ", err)

print("=====")

try:
    print(authenticate_user("dewkong12", "dewkong321"))
except TypeError as err:
    print(err)
