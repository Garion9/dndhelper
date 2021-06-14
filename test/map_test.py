from Database_Module import DatabaseHandler
from Campaign_Module import *

world = WorldMap.map_new(5, 3, (0, 0))
print(world.grid)
print(world.current_field)
print(world.visited_fields)
world.move((0, 1))
print(world.current_field)
print(world.visited_fields)
world.move((0, 2))
print(world.current_field)
print(world.visited_fields)
world.move((1, 2))
print(world.current_field)
print(world.visited_fields)

world.add_field_note((2, 2), "Tutaj jest drzewiec")
print(world.grid)
print(world.get_field_note((2, 2)))

DatabaseHandler.insert_campaign(world)
#for db_world_map in DatabaseHandler.get_world_maps_collection():
#    world_map = WorldMap.map_from_db_entry(db_world_map)
#    print(world_map.grid)
#    print(world_map.visited_fields)
#    print(world_map.current_field)