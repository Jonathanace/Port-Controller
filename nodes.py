from states import Grid
class Node:
    def __init__(self, ship, holdingArea = None, trucks = False, previousNode = None):
        self.ship = ship
        self.holdingArea = holdingArea
        self.trucks = trucks
        self.previousNode = previousNode
        self.childNodes = []
        