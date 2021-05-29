from Character_Module import *
from Dice_Module import *
from Database_Module import *

test_character = Character.character_new("Garion", "Garion", "Druid", "Dragonborn", "CG", "Unknown", 14, 10, 12, 14, 16, 8, 14, 30, 8,
                           "traits", "languages", "equipments", "notes")

another_character = Character.character_new("Dewkong", "Dewkong", "Barbarian", "Dwarf", "NG", "Miner", 14, 10, 12, 14, 16, 8, 14, 30, 12,
                              "traits", "languages", "equipments", "notes", level=1)

#print(test_character)
#print("==============")
#print(another_character)
#print("==============")

#another_character.add_exp(another_character.get_exp_for_next_level() + 10)
#print(another_character)
#print("==============")

#print(another_character.level)
#print(another_character.exp)
#print(another_character.max_hit_points)
#print(another_character.no_hit_dice)

#print("==============")

#print(test_character.__dict__)
#print(vars(another_character))

#Database_Handler.insert_character(test_character)
#Database_Handler.print_characters_collection()
#print("==============")
#Database_Handler.insert_character(another_character)
#Database_Handler.print_characters_collection()

characters = DatabaseHandler.get_characters_collection()
for character_db in characters:
    character = Character.character_from_db_entry(character_db)
    print(character)
    print("==============")
