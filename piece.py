# Class for each piece
class Piece:
    def __init__(self, name):
        self.name = name
        self.has_eaten = False

    # Returns piece name
    def get_name(self):
        return self.name

    # Return piece position
    def get_position(self):
        return self.name[:-2]

    # Return piece color
    def get_color(self):
        return self.name[-2]

    # Set a position for a piece
    def set_position(self, new_position):
        position_index = 1 if len(self.name) == 3 else 2
        self.name = str(new_position) + self.name[position_index:]

