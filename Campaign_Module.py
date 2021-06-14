from bson.objectid import ObjectId

class Campaign:
    def __init__(self, campaign_data):
        self._id = ObjectId()
        self.campaign_name = None
        self.players = None
        self.battlemap_id = None
        for key in campaign_data:
            setattr(self, key, campaign_data[key])

    # method for creating class instance of a brand new campaign
    @classmethod
    def campaign_new(cls, campaign_name, battlemap_id):
        campaign_data = {"campaign_name": campaign_name, "players": [], "battlemap_id": battlemap_id}
        campaign = cls(campaign_data)
        return campaign

    # method for creating class instance from a database entry
    @classmethod
    def campaign_from_db_entry(cls, db_entry):
        return cls(db_entry)

    def get_id(self):
        return self._id

    def add_player(self, user_login):
        if user_login not in self.players:
            self.players.append(user_login)