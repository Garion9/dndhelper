from Monster_Module import *
from Database_Module import *

test_monster1 = Monster.monster_new("Manticore", "Monstrosity", 16, 80, 50, 18, 18, 16, 12, 14, 8, 7, "Very dangerous beast.")
test_monster2 = Monster.monster_new("Red dragon", "Beast", 18, 120, 50, 20, 16, 20, 14, 16, 8, 12, "Even more dangerous beast.")

#print(test_monster1)
#print(test_monster2)

#DatabaseHandler.insert_monster(test_monster1)
#DatabaseHandler.insert_monster(test_monster2)

monsters = DatabaseHandler.get_monsters_collection()
for monster in monsters:
    monster_from_db = Monster.monster_from_db_entry(monster)
    print(monster_from_db)
    print("=====")
