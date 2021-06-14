from collections import OrderedDict

from bson.objectid import ObjectId

class BattleMap:
    def __init__(self, map_data):
        self._id = ObjectId()
        self.rows = None
        self.columns = None
        self.active_tokens = None
        for key in map_data:
            setattr(self, key, map_data[key])

    # method for creating class instance of a brand new map
    @classmethod
    def battlemap_new(cls, rows, columns):
        map_data = {"rows": rows, "columns": columns, "active_tokens": OrderedDict()}
        battlemap = cls(map_data)
        return battlemap

    # method for creating class instance from a database entry
    @classmethod
    def battlemap_from_db_entry(cls, db_entry):
        map_data = {"_id": db_entry["_id"],
                    "rows": db_entry["rows"],
                    "columns": db_entry["columns"],
                    "active_tokens": OrderedDict([(tuple(key), tuple(value)) for key, value in zip(db_entry["token_keys"], db_entry["token_values"])]) }
        return cls(map_data)

    def map_to_db_entry(self):
        db_entry = {"_id": self._id,
                    "rows": self.rows,
                    "columns": self.columns,
                    "token_keys": list(self.active_tokens.keys()),
                    "token_values": list(self.active_tokens.values())}
        return db_entry

    def __str__(self):
        return "ID: " + str(self._id) + "\n" +\
               "rows: " + str(self.rows) + "\n" +\
               "columns: " + str(self.columns) + "\n" +\
               "active tokens: " + str(self.active_tokens) + "\n"

    def get_id(self):
        return self._id

    def add_token(self, x_position, y_position, color, label, user_login):
        self.active_tokens[(x_position, y_position)] = (color, label, user_login)

    def remove_token(self, x_position, y_position):
        self.active_tokens.pop((x_position, y_position))

    def move_token(self, x_old, y_old, x_new, y_new):
        self.active_tokens[(x_new, y_new)] = self.active_tokens.pop((x_old, y_old))

    def get_token_color(self, x_position, y_position):
        return self.active_tokens[(x_position, y_position)][0]

    def get_token_label(self, x_position, y_position):
        return self.active_tokens[(x_position, y_position)][1]

    def get_token_owner(self, x_position, y_position):
        return self.active_tokens[(x_position, y_position)][2]

    def get_active_tokens(self):
        return self.active_tokens

    def resize(self, rows, columns):
        self.rows = rows
        self.columns = columns
        for key in self.active_tokens.keys():
            if key[0] >= rows or key[1] >= columns:
                self.active_tokens.pop(key)
