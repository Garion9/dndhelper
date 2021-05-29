from bson.objectid import ObjectId

class WorldMap:
    def __init__(self, map_data):
        self._id = ObjectId()
        self.grid = None
        self.visited_fields = None
        self.current_field = None
        for key in map_data:
            setattr(self, key, map_data[key])

    # method for creating class instance of a brand new map
    @classmethod
    def map_new(cls, x, y, starting_field):
        grid = [["" for _ in range(x)] for _ in range(y)]
        visited_field = [starting_field]
        map_data = {"grid": grid, "visited_fields": visited_field, "current_field": starting_field}
        world_map = cls(map_data)
        return world_map

    # method for creating class instance from a database entry
    @classmethod
    def map_from_db_entry(cls, db_entry):
        return cls(db_entry)

    def move(self, new_field):
        if 0 <= new_field[0] <= len(self.grid[0])-1 and 0 <= new_field[1] <= len(self.grid)-1:
            if self.current_field not in self.visited_fields:
                self.visited_fields.append(self.current_field)
            self.current_field = new_field

    def add_field_note(self, field, note):
        if 0 <= field[0] <= len(self.grid[0]) - 1 and 0 <= field[1] <= len(self.grid) - 1:
            self.grid[field[0]][field[1]] = note

    def get_field_note(self, field):
        if 0 <= field[0] <= len(self.grid[0]) - 1 and 0 <= field[1] <= len(self.grid) - 1:
            return self.grid[field[0]][field[1]]
