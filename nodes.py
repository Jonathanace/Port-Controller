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
    # index [x,y]
    def check_above(self,index: tuple[int,int]) -> bool:
        if self.ship[index[0]][index[1]].isEmpty == True:
            return True
        return False
    # checks which possibe spot they can move to
    #index[x,y]
    def check_avaiable(self,index: tuple[int,int]):
        available_moves = []
        for i in range(len(self.ship[0])):
            if i == index[0]:
                continue
            j = len(self.ship[0]) -1 
            while j >= 0:
                if self.ship[i][j].isEmpty == False:
                    available_moves.append([i,j+1])
                    break
                if j == 0:
                    available_moves.append([i,j])
                    break
                j+-1
        return available_moves

with open(f"SilverQueen.txt") as f:
    res = parse_manifest(f.read())
shipSilverQueen  = toGrid(res)
startNode = Node(shipSilverQueen)
print(startNode.check_above([1,2]))