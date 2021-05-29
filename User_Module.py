from passlib.context import CryptContext
from Database_Module import *

pwd_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=30000
    )

class User:
    def __init__(self, login, nickname, password):
        self.login = login
        self.nickname = nickname
        self.password = password

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
