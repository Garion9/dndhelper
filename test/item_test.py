from Item_Module import *
from Database_Module import *


test_item = Item.item_new("Testowy przedmiot 1", "To jest opis testowego przedmiotu 1")
#print(test_item)

#DatabaseHandler.insert_item(test_item)

items = DatabaseHandler.get_items_collection()
for item in items:
    item_from_db = Item.item_from_db_entry(item)
    print(item_from_db)
