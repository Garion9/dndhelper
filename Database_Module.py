import pymongo

class DatabaseHandler:
    client = pymongo.MongoClient(
        "mongodb+srv://Garion:hwTFr1zLhbaUDXbX@clusterdndhelper.ik5cn.mongodb.net/DBDnDHelper?retryWrites=true&w=majority")
    db = client["DBDnDHelper"]
    characters_collection = db["Characters"]
    users_collection = db["Users"]
    monsters_collection = db["Monsters"]
    items_collection = db["Items"]
    world_maps_collection = db["World Maps"]

    @classmethod
    def insert_character(cls, character):
        #db_character = character.__dict__
        db_character = vars(character)
        cls.characters_collection.insert_one(db_character)

    @classmethod
    def get_characters_collection(cls):
        return cls.characters_collection.find()

    @classmethod
    def print_characters_collection(cls):
        for character in cls.characters_collection.find():
            print(character)

    @classmethod
    def insert_user(cls, user):
        db_user = vars(user)
        cls.users_collection.insert_one(db_user)

    @classmethod
    def get_user(cls, login):
        return cls.users_collection.find_one({"login": login})

    @classmethod
    def insert_item(cls, item):
        db_item = vars(item)
        cls.items_collection.insert_one(db_item)

    @classmethod
    def get_items_collection(cls):
        return cls.items_collection.find()

    @classmethod
    def insert_monster(cls, monster):
        db_monster = vars(monster)
        cls.monsters_collection.insert_one(db_monster)

    @classmethod
    def get_monsters_collection(cls):
        return cls.monsters_collection.find()

    @classmethod
    def insert_world_map(cls, world_map):
        db_world_map = vars(world_map)
        cls.world_maps_collection.insert_one(db_world_map)

    @classmethod
    def get_world_maps_collection(cls):
        return cls.world_maps_collection.find()
