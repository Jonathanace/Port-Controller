from states import Grid 
from states import to_grid
from utils import parse_manifest
from utils import Item
class Node:
    def __init__(self, ship, holding_area = None, trucks = False, previous_node = None):
        self.ship = ship
        self.holding_area = holding_area
        self.trucks = trucks
        self.previous_node = previous_node
        self.child_nodes = []
    # checks if there is anything above the container, will be used in the move function
    # index [x,y]
    def check_above(self,index: tuple[int,int]) -> bool:
        if index[0] == 7:
            return True
        if self.ship[index[0] + 1][index[1]].is_empty == True:
            return True
        return False
    # checks which possibe spot they can move to
    #index[x,y]
    def check_available(self,index: tuple[int,int]):
        available_moves = []
        temp = self.ship[index[0], index[1]]
        print(temp.position, temp.name)
        #columns
        for j in range(len(self.ship[0])):
            if j == index[1]:
                    continue
            #rows
            i = len(self.ship) -1 
            while i >= 0:
                print(i, j, self.ship[i][j].position, self.ship[i][j].name)
                if self.ship[i][j].is_empty == False:
                    print(self.ship[i][j].position, self.ship[i][j].name)
                    if i + 1 < 8:
                        available_moves.append([i+1,j])
                    break
                if i == 0:
                    print(self.ship[i][j].position, self.ship[i][j].name)
                    available_moves.append([i,j])
                    break
                i = i -1
        # print(available_moves)
        return available_moves
