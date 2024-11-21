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
        if self.ship[index[0]][index[1]+1].isEmpty == True:
            return True
        return False
    # checks which possibe spot they can move to
    #index[x,y]
    def check_avaiable(self,index: tuple[int,int]):
        available_moves = []
        #columns
        for j in range(len(self.ship[0])):
            if j == index[1]:
                    continue
            #rows
            i = len(self.ship) -1 
            while i >= 0:
                print(i, j, self.ship[i][j].position, self.ship[i][j].name)
                if self.ship[i][j].isEmpty == False:
                    print(self.ship[i][j].position, self.ship[i][j].name)
                    available_moves.append([i+1,j])
                    break
                if j == 0:
                    print(self.ship[i][j].position, self.ship[i][j].name)
                    available_moves.append([i,j])
                    break
                i = i -1
                
        print(available_moves)
        return available_moves

with open(f"SilverQueen.txt") as f:
    res = parse_manifest(f.read())
shipSilverQueen  = toGrid(res)
startNode = Node(shipSilverQueen)
print(startNode.check_avaiable([1,2]))
