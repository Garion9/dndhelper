from bson.objectid import ObjectId
from passlib.context import CryptContext
from Database_Module import *

pwd_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=30000
    )

class User:
    def __init__(self, user_data):
        self._id = ObjectId()
        self.login = None
        self.nickname = None
        self.password = None
        for key in user_data:
            setattr(self, key, user_data[key])

    @classmethod
    def user_new(cls, login, nickname, password):
        user_data = {"login": login, "nickname": nickname, "password": password}
        user = cls(user_data)
        return user

    @classmethod
    def user_from_db_entry(cls, db_entry):
        return cls(db_entry)

# throws pymongo.errors.DuplicateKeyError
def register_user(login, nickname, password):
    password = pwd_context.encrypt(password)
    user = User(login, nickname, password)
    DatabaseHandler.insert_user(user)

# throws TypeError
def authenticate_user(login, password):
    user = DatabaseHandler.get_user(login)
    if user is None:
        raise TypeError("User with this login doesn't exist.")
    else:
        return pwd_context.verify(password, user["password"])
