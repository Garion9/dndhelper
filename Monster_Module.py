from bson.objectid import ObjectId

class Monster:
    # dictionary in which keys are challenge ratings (or CR for short) of monsters and values are pairs (tuples)
    # containing experience value and proficiency bonus (in that order) of a monster of given challenge rating, so:
    # exp_val of a monster is challenge_table[CR][0]
    # and their prof_bonus is challenge_table[CR][1]
    challenge_table = {0: (0, 2), 0.125: (25, 2), 0.25: (50, 2), 0.5: (100, 2),
                       1: (200, 2), 2: (450, 2), 3: (700, 2), 4: (1100, 2),
                       5: (1800, 3), 6: (2300, 3), 7: (2900, 3), 8: (3900, 3),
                       9: (5000, 4), 10: (5900, 4), 11: (7200, 4), 12: (8400, 4),
                       13: (10000, 5), 14: (11500, 5), 15: (13000, 5), 16: (15000, 5),
                       17: (18000, 6), 18: (2000, 6), 19: (22000, 6), 20: (25000, 6),
                       21: (33000, 7), 22: (41000, 7), 23: (50000, 7), 24: (62000, 7),
                       25: (75000, 8), 26: (90000, 8), 27: (105000, 8), 28: (120000, 8),
                       29: (135000, 9), 30: (155000, 9)}

    def __init__(self, monster_data):
        self._id = ObjectId()
        self.name = None
        self.family = None
        self.armor_class = None
        self.max_hit_points = None
        self.speed = None
        self.strength = None
        self.dexterity = None
        self.constitution = None
        self.intelligence = None
        self.wisdom = None
        self.charisma = None
        self.challenge_rating = None
        self.description = None
        for key in monster_data:
            setattr(self, key, monster_data[key])

    # method for creating class instance of a brand new monster
    @classmethod
    def monster_new(cls, name, family, armor_class, max_hit_points, speed, strength, dexterity, constitution,
                    intelligence, wisdom, charisma, challenge_rating, description):
        monster_data = {"name": name,
                        "family": family,
                        "armor_class": armor_class,
                        "max_hit_points": max_hit_points,
                        "speed": speed,
                        "strength": strength,
                        "dexterity": dexterity,
                        "constitution": constitution,
                        "intelligence": intelligence,
                        "wisdom": wisdom,
                        "charisma": charisma,
                        "challenge_rating": challenge_rating,
                        "description": description}
        return cls(monster_data)

    # method for creating class instance from a database entry
    @classmethod
    def monster_from_db_entry(cls, db_entry):
        return cls(db_entry)

    def __str__(self):
        return "ID: " + str(self._id) \
               + "\nName: " + self.name \
               + "\nFamily: " + self.family \
               + "\nArmor class: " + str(self.armor_class) + \
               "\nMax hit points: " + str(self.max_hit_points) + \
               "\nSpeed: " + str(self.speed) + \
               "\nStrength: " + str(self.strength) + \
               "\nDexterity: " + str(self.dexterity) + \
               "\nConstitution: " + str(self.constitution) + \
               "\nIntelligence: " + str(self.intelligence) + \
               "\nWisdom: " + str(self.wisdom) + \
               "\nCharisma: " + str(self.charisma) + \
               "\nChallenge rating: " + str(self.challenge_rating) + \
               "\nDescription: " + self.description

    def get_attribute_modifier(self, attribute):
        return (getattr(self, attribute)-10)//2

    def get_strength_modifier(self):
        return self.get_attribute_modifier("strength")

    def get_dexterity_modifier(self):
        return self.get_attribute_modifier("dexterity")

    def get_constitution_modifier(self):
        return self.get_attribute_modifier("constitution")

    def get_intelligence_modifier(self):
        return self.get_attribute_modifier("intelligence")

    def get_wisdom_modifier(self):
        return self.get_attribute_modifier("wisdom")

    def get_charisma_modifier(self):
        return self.get_attribute_modifier("charisma")