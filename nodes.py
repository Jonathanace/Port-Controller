from states import Grid 
from states import to_grid
from utils import parse_manifest
from utils import Item
class Node:
    def __init__(self, ship, holding_area = None, trucks = False, previous_node = None, crane_pos = "Start"):
        self.ship = ship
        self.holding_area = holding_area
        self.trucks = trucks
        self.previous_node = previous_node
        self.child_nodes = []
        self.crane_pos = crane_pos
    
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
        column = index[1]
        l = column - 1
        r = column + 1
        while l >= 0 or r < len(self.ship[0]):
            if l >= 0:
                left_temp = self.check_column(l)
                available_moves.append(left_temp)
                l -= 1
            if r < len(self.ship[0]):
                right_temp = self.check_column(r)
                available_moves.append(right_temp)
                r += 1
        return available_moves

    #Helper function that finds the highest empty square in a column
    def check_column(self, col: int):
        curr = self.ship
        n = 7
        res = tuple([0,0])
        while n >= 0:
            if curr[n][col].is_empty == False:
                if n + 1 < 8:
                    res = tuple([n + 1, col])
                    return res
            if n == 0:
                res = tuple([n, col])
                return res
            n -= 1
        res = tuple([n, col])
        return res
    def check_aviable_load(self):
        available_moves = []
        for j in range(len(self.ship[0])):
            available_moves.append(self.check_column(j))
        return available_moves

                       
# with open(f"SilverQueen.txt") as f:
#     res = parse_manifest(f.read())
# shipSilverQueen  = to_grid(res)
# startNode = Node(shipSilverQueen)
# print(startNode.check_available([1,1]))