# Here is the basic outline of what the board will look like for reference
#     1    2    3    4    5    6    7    8    9
# A ["-"]["-"]["-"]["-"]["-"]["-"]["-"]["-"]["-"]
# B ["-"]["-"]["-"]["-"]["-"]["-"]["-"]["-"]["-"]
# C ["-"]["o"]["-"]["-"]["-"]["-"]["-"]["-"]["-"]
# D ["-"]["o"]["-"]["-"]["-"]["-"]["-"]["-"]["-"]
# E ["-"]["o"]["-"]["-"]["-"]["-"]["-"]["-"]["-"]
# F ["-"]["x"]["-"]["-"]["-"]["-"]["-"]["-"]["-"]
# G ["-"]["-"]["-"]["-"]["-"]["-"]["-"]["-"]["-"]
# H ["-"]["-"]["-"]["-"]["-"]["-"]["-"]["-"]["-"]
# I ["-"]["-"]["-"]["-"]["-"]["-"]["-"]["-"]["-"]

# Empty square: -
# Boat square: o
# Hit square: x
# Missed square: 
# Complete ship gone: #

# Each player will have:
#   3 1-tile ships : 3 tiles
#   4 2-tile ships : 8 tiles
#   4 3-tile ships : 12 tiles
#   3 4-tile ships : 12 tiles
# therefore 35 tiles overall



class Board:
    
    def __init__(self):
        # Holds the board
        self.__board = [["-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
                        ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
                        ["-", "o", "-", "-", "-", "-", "-", "-", "-", "-"],
                        ["-", "o", "-", "-", "-", "-", "-", "-", "-", "-"],
                        ["-", "x", "-", "-", "-", "-", "-", "-", "-", "-"],
                        ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
                        ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
                        ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
                        ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
                        ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-"]]

        # Holds coordinates already targeted, as tuples
        self.__targetedCoords = set()

        # Holds every boat and the coordinates of said boat - every boat stored in a list, then each boat has a dictionary of 
        # tiles, with bools to show if theyeve been hit or not
        # Coordinates are stord as indexes, NO LETTERS THEY HAVE ALREADY BEEN CONVERTED AT THIS POINT
        self.__boats = []

    # Gets rid of the 0 index problem so coordinates 1-10 and A-J can be used
    # Returned in a 2-variable format where [0] is x and [1] is y
    def CoordToBoard(self, coordinate):
        return coordinate[0] - 1, ord(coordinate[1]) - 65
    
    # Displays the board row by row without any quotation marks
    def DisplayBoard(self):
        for row in self.__board:
            print(*row)

    # Checks if the chosen coordinate is free or not
    # Only to be used at the start of the game when boats are initially being placed
    # By this point, all other input has been sanitised so no checking is needed
    # Returns false if tile is occupied, returns true if tile is free
    def CheckIfFree(self, coordinate):
        x, y = self.CoordToBoard(coordinate)
        for boat in self.__boats:
            if (x, y) in boat.keys():
                return False
        return True
            


    # Takes in coordinates for an attack
    # Checks if the coordinates are valid. If not, returns "indexError"
    # Checks if the coordinates inputted have already been hit. If they are, returns "chooseError"
    # If nothing was hit, returns false
    # If a tile has hit, returns "hit"
    # If a whole ship is therefore sunk, returns "wholeHit"
    def TakeShot(self, coordinate):
        x, y = self.CoordToBoard(coordinate)
        # Checks valid target
        try:
            target = self.__board[x][y]
        except IndexError:
            return "indexError"
        # Checks if already hit
        if (x, y) in self.__targetedCoords:
            return "chooseError"
        # Checks emtpy square
        elif target == "-":
            self.__board[x][y] = " "
            self.__targetedCoords.add((x, y))
            return False
        # Checks for a boat tile hit. Then checks if the whole boat has been destroyed, or only part of it. Does this through 
        elif target == "o":
            # Initially checks which boat the coordinate belongs to
            for boat in self.__boats:
                if target in boat:
                    targetBoat = boat
            # Makes that coordinate hit
            boat.update({(x, y) : 0})
            # Checks to see if all of the coordinates are hit or not. If no, turns to "x", if yes, boat turns to "#"
            for hit in targetBoat.values():
                if hit == 1:
                    self.__board[x][y] = "x"
                    return "hit"
            # Only gets to this bit if the whole boat has been destroyed
            for coordinate in targetBoat.keys():
                self.board[coordinate[0], coordinate[1]] = "#"
                return "wholeHit"
 
    # Takes in an initial coordinate for the start of the boat, the type of boat, an orientation for the boat, and a number for the type of boat
    # If the coordinates are invalid/go out of range, return "indexError" /
    # Be careful to make sure that boats do not loop around the screen
    # If the key pressed is wrong, returns "keyError" /
    # If the boat would overlap another boat, returns "boatError" /

    # Coordinate is passed in as letters & numbers as likely to be higher level
    # Boat Type passed in as integer (1, 2, 3, or 4) to indicate the length of the boat
    # Orientation is passed in as: "w" (up), "a" (left), "s" (down), or "d" (right)
    def PlaceBoat(self, coordinate, boatType, orientation, number):
        x, y = self.CoordToBoard(coordinate)
        # This validates both the initial coordinate, the rotation, and whether the boat may overlap another boat
        match orientation:
            case "w":
                for i in range(boatType):
                    nextX, nextY = self.CoordToBoard((x, chr(ord(y) - i)))
                    try:
                        if not self.CheckIfFree((nextX, nextY)):
                            return "boatError"
                    except IndexError:
                        return "indexError"
            case "a":
                for i in range(boatType):
                    nextX, nextY = self.CoordToBoard((x - 1, y))
                    try:
                        if not self.CheckIfFree((nextX, nextY)):
                            return "boatError"
                    except IndexError:
                        return "indexError"
            case "s":
                for i in range(boatType):
                    nextX, nextY = self.CoordToBoard((x, chr(ord(y) + i)))
                    try:
                        if not self.CheckIfFree((nextX, nextY)):
                            return "boatError"
                    except IndexError:
                        return "indexError"
            case "d":
                for i in range(boatType):
                    nextX, nextY = self.CoordToBoard((x + 1, y))
                    try:
                        if not self.Checkq((nextX, nextY)):
                            return "boatError"
                    except IndexError:
                        return "indexError"
            case _:
                return "keyError"
        # SANITISATION IS ALL DONE!!
        # Now have to repeat match case as above, except placing - cannot place at same time as check otherwise would have to
        # go about deleting entries
        # First finding out how to name the boat
        boat = {"name" : f"{number}boat-length{boatType}"}
        match orientation:
            case "w":
                
                


        





board = Board();
result = board.TakeShot([1, "A"])
board.DisplayBoard()