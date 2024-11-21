from states import Grid 
from states import toGrid
from utils import parse_manifest
from utils import Item
class Node:
    def __init__(self, ship, holdingArea = None, trucks = False, previousNode = None):
        self.ship = ship
        self.holdingArea = holdingArea
        self.trucks = trucks
        self.previousNode = previousNode
        self.childNodes = []
    # checks if there is anything above the container, will be used in the move function
    def check_above(self,index: tuple[int,int]) -> bool:
        if self.ship[index[0]][index[1]].isEmpty == True:
            return True
        return False

with open(f"SilverQueen.txt") as f:
    res = parse_manifest(f.read())
shipSilverQueen  = toGrid(res)
startNode = Node(shipSilverQueen)
print(startNode.check_above([1,2]))