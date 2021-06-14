from bson.objectid import ObjectId

class Spell:
    def __init__(self, item_data):
        self._id = ObjectId()
        self.name = None
        self.description = None
        for key in item_data:
            setattr(self, key, item_data[key])

    # method for creating class instance of a brand new spell
    @classmethod
    def spell_new(cls, name, description):
        spell_data = {"name": name, "description": description}
        spell = cls(spell_data)
        return spell

    # method for creating class instance from a database entry
    @classmethod
    def spell_from_db_entry(cls, db_entry):
        return cls(db_entry)

    def __str__(self):
        return "ID: " + str(self._id) \
               + "\nName: " + self.name \
               + "\nDescription: " + self.description
