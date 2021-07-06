import pymongo

class DatabaseHandler:
    client = pymongo.MongoClient(
        "mongodb+srv://Garion:hwTFr1zLhbaUDXbX@clusterdndhelper.ik5cn.mongodb.net/DBDnDHelper?retryWrites=true&w=majority", ssl=True, ssl_cert_reqs="CERT_NONE")
    db = client["DBDnDHelper"]
    characters_collection = db["Characters"]
    users_collection = db["Users"]
    monsters_collection = db["Monsters"]
    items_collection = db["Items"]
    campaigns_collection = db["Campaigns"]
    battlemaps_collection = db["BattleMaps"]
    spells_collection = db["Spells"]

    @classmethod
    def insert_character(cls, character):
        #db_character = character.__dict__
        db_character = vars(character)
        cls.characters_collection.insert_one(db_character)

    @classmethod
    def update_character(cls, character):
        query = {"_id": character.get_id()}
        new_values = {"$set": vars(character)}
        cls.characters_collection.update_one(query, new_values)

    @classmethod
    def get_characters_collection(cls):
        return cls.characters_collection.find()

    @classmethod
    def print_characters_collection(cls):
        for character in cls.characters_collection.find():
            print(character)

    @classmethod
    def get_character(cls, _id):
        return cls.characters_collection.find_one({"_id": _id})

    @classmethod
    def insert_user(cls, user):
        db_user = vars(user)
        cls.users_collection.insert_one(db_user)

    @classmethod
    def get_user(cls, login):
        return cls.users_collection.find_one({"login": login})

    @classmethod
    def get_users_collection(cls):
        return cls.users_collection.find()

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
    def insert_campaign(cls, campaign):
        db_campaign = vars(campaign)
        cls.campaigns_collection.insert_one(db_campaign)

    @classmethod
    def get_campaigns_collection(cls):
        return cls.campaigns_collection.find()

    @classmethod
    def get_campaign(cls, _id):
        return cls.campaigns_collection.find_one({"_id": _id})

    @classmethod
    def update_campaign(cls, campaign):
        query = {"_id": campaign.get_id()}
        new_values = {"$set": vars(campaign)}
        cls.campaigns_collection.update_one(query, new_values)

    @classmethod
    def insert_battlemap(cls, battlemap):
        cls.battlemaps_collection.insert_one(battlemap.map_to_db_entry())

    @classmethod
    def get_battlemap(cls, _id):
        return cls.battlemaps_collection.find_one({"_id": _id})

    @classmethod
    def update_battlemap(cls, battlemap):
        cls.battlemaps_collection.update_one({"_id": battlemap.get_id()}, {"$set": battlemap.map_to_db_entry()})

    @classmethod
    def get_spells_collection(cls):
        return cls.spells_collection.find()

    @classmethod
    def insert_spell(cls, spell):
        db_spell = vars(spell)
        cls.spells_collection.insert_one(db_spell)
