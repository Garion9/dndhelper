from bson.objectid import ObjectId

import Dice_Module as Dice

class Character:
    # amounts of experience required for next level starting with level 2
    experience_table = [300,    900,   2700,   6500,
                        14000,  23000,  34000,  48000,  64000,
                        85000, 100000, 120000, 140000, 165000,
                        195000, 225000, 265000, 305000, 355000]

    def __init__(self, character_data):
        self._id = ObjectId()
        self.user = None
        self.name = None
        self.c_class = None
        self.level = None
        self.race = None
        self.alignment = None
        self.exp = None
        self.background = None
        self.inspiration = None
        self.strength = None
        self.dexterity = None
        self.constitution = None
        self.intelligence = None
        self.wisdom = None
        self.charisma = None
        self.skill_proficiency = None
        self.saving_throw_proficiency = None
        self.armor_class = None
        self.speed = None
        self.hit_dice_faces = None
        self.no_hit_dice = None
        self.max_hit_points = None
        self.current_hit_points = None
        self.death_saving_throw_failures = None
        self.death_saving_throw_successes = None
        self.features_traits = None
        self.proficiencies_languages = None
        self.equipment = None
        self.notes = None
        self.spells_list = None
        for key in character_data:
            setattr(self, key, character_data[key])

    # method for creating class instance of a brand new character
    @classmethod
    def character_new(cls, user, name, c_class, race, alignment, background, strength, dexterity, constitution,
                      intelligence, wisdom, charisma, armor_class, speed, hit_dice_faces,
                      features_traits, proficiencies_languages, equipment, notes, spells,
                      inspiration=0, level=1, exp=0, skill_proficiency=None, saving_throw_proficiency=None, max_hit_points=0):
        if saving_throw_proficiency is None:
            saving_throw_proficiency = []
        if skill_proficiency is None:
            skill_proficiency = []
        character_data = {"user": user,
                          "name": name,
                          "c_class": c_class,
                          "level": level,
                          "race": race,
                          "alignment": alignment,
                          "exp": exp,
                          "background": background,
                          "inspiration": inspiration,
                          "strength": strength,
                          "dexterity": dexterity,
                          "constitution": constitution,
                          "intelligence": intelligence,
                          "wisdom": wisdom,
                          "charisma": charisma,
                          "skill_proficiency": skill_proficiency,
                          "saving_throw_proficiency": saving_throw_proficiency,
                          "armor_class": armor_class,
                          "speed": speed,
                          "hit_dice_faces": hit_dice_faces,
                          "no_hit_dice": level,
                          "max_hit_points": max_hit_points,
                          "current_hit_points": max_hit_points,
                          "death_saving_throw_failures": 0,
                          "death_saving_throw_successes": 0,
                          "features_traits": features_traits,
                          "proficiencies_languages": proficiencies_languages,
                          "equipment": equipment,
                          "notes": notes,
                          "spells_list": spells}
        character = cls(character_data)
        character.initialize_max_hp()
        character.current_hit_points = character.max_hit_points
        return character

    # method for creating class instance from a database entry
    @classmethod
    def character_from_db_entry(cls, db_entry):
        return cls(db_entry)

    def __str__(self):
        return "ID: " + str(self._id) + "\nUser: " + self.user + "\nName: " + self.name + "\nCharacter class: " + self.c_class + \
               "\nCharacter level: " + str(self.level) +\
               "\nRace" + self.race + "\nAlignment: " + self.alignment + "\nExperience: " + str(self.exp) + \
               "\nBackground: " + self.background + "\nInspiration: " + str(self.inspiration) + \
               "\nStrength: " + str(self.strength) + "\nDexterity: " + str(self.dexterity) + \
               "\nConstitution: " + str(self.constitution) + "\nIntelligence: " + str(self.intelligence) + \
               "\nWisdom: " + str(self.wisdom) + "\nCharisma: " + str(self.charisma) + \
               "\nSkill proficiencies: " + str(self.skill_proficiency) + \
               "\nSaving throw proficiencies: " + str(self.saving_throw_proficiency) + \
               "\nArmor class: " + str(self.armor_class) + "\nSpeed: " + str(self.speed) + \
               "\nHit die faces: " + str(self.hit_dice_faces) + "\nNumber of hit dice: " + str(self.no_hit_dice) + \
               "\nMax hit points: " + str(self.max_hit_points) + "\nCurrent hit points: " + str(self.current_hit_points) +\
               "\nDeath saving throw failures: " + str(self.death_saving_throw_failures) + \
               "\nDeath saving throw successes: " + str(self.death_saving_throw_successes) + \
               "\nOther features and traits: " + self.features_traits + \
               "\nOther proficiencies and languages: " + self.proficiencies_languages + \
               "\nEquipment: " + self.equipment + \
               "\nNotes: " + self.notes + \
               "\nSpells list: " + self.spells_list

    def get_id(self):
        return self._id

    def get_proficiency_bonus(self):
        return ((self.level-1)//4)+2

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

    def add_skill_proficiency(self, skill):
        self.skill_proficiency.append(skill)

    def add_saving_throw_proficiency(self, attribute):
        self.saving_throw_proficiency.append(attribute)

    def add_spell(self, spell):
        self.spells_list.append(spell)

    def get_skill_check_modifier(self, attribute, skill):
        result = self.get_attribute_modifier(attribute)
        if skill in self.skill_proficiency:
            result += self.get_proficiency_bonus()
        return result

    def get_passive_perception(self):
        return 8 + self.get_skill_check_modifier("wisdom", "perception")

    def get_saving_throw_modifier(self, attribute):
        result = self.get_attribute_modifier(attribute)
        if attribute in self.saving_throw_proficiency:
            result += self.get_proficiency_bonus()
        return result

    def get_exp_for_next_level(self):
        if self.level < 20:
            return self.experience_table[self.level-1]
        else:
            return self.experience_table[18]

    def add_exp(self, exp_amount):
        self.exp += exp_amount
        while self.exp >= self.get_exp_for_next_level():
            self.exp -= self.get_exp_for_next_level()
            self.level_up()

    def level_up(self):
        if self.level >= 20:
            return
        else:
            self.level += 1
            self.increase_max_hp()
            self.current_hit_points += self.max_hit_points - self.current_hit_points
            self.no_hit_dice += 1

    def increase_max_hp(self):
        self.max_hit_points += Dice.roll_dice(1, self.hit_dice_faces)[0]
        self.max_hit_points += self.get_constitution_modifier()

    def initialize_max_hp(self):
        self.max_hit_points = self.hit_dice_faces + self.get_constitution_modifier()
        for lvl in range(2, self.level+1):
            self.increase_max_hp()
