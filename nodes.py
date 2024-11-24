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
        if self.ship[index[0] + 1][index[1]].is_empty == True:
            return True
        return False
    # checks which possibe spot they can move to
    #index[x,y]
    def check_available(self,index: tuple[int,int]):
        available_moves = []
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
                    available_moves.append([i+1,j])
                    break
                if i == 0:
                    print(self.ship[i][j].position, self.ship[i][j].name)
                    available_moves.append([i,j])
                    break
                i = i -1
                
        print(available_moves)
        return available_moves
    #unloading/loading functions 
    def find_item(self, item):
        index_list = []
        for i in range(len(self.ship)):
            for j in range(len(self.ship)):
                if self.ship[i][j].name == item:
                    index_list.append([i,j])
        if len(index_list) == 0:
            return index_list
        return index_list
    def item_amount(self, item):
        amount = 0
        for i in range(len(self.ship)):
            for j in range(len(self.ship)):
                if self.ship[i][j].name == item:
                    amount+=1
        return amount
    def unload_ship(self, itemlist):
        #indexes for every item on the ship
        for item in itemlist:
            possible_indexes = self.find_item(item)
            if len(possible_indexes) == 0:
                break
            for index in possible_indexes:
                if self.check_above(index):
                    #print(self.ship[index[0],index[1]].name)
                    temp_ship = self.ship
                    temp_ship[index[0],index[1]].set_empty()
                    child_node = Node(temp_ship, previous_node= self)
                    self.child_nodes.append(child_node)
                    #print(self.ship[index[0],index[1]].name)
                    print(f"Moved {item} off of ship from location:  {index[0] + 1} , {index[1] + 1}" )
        return
    def check_available_load(self):
        available_moves = []
        for j in range(len(self.ship[0])):
            #rows
            i = len(self.ship) -1 
            while i >= 0:
                print(i, j, self.ship[i][j].position, self.ship[i][j].name)
                if self.ship[i][j].is_empty == False:
                    print(self.ship[i][j].position, self.ship[i][j].name)
                    available_moves.append([i+1,j])
                    break
                if i == 0:
                    print(self.ship[i][j].position, self.ship[i][j].name)
                    available_moves.append([i,j])
                    break
                i = i -1
        return available_moves
    def load_ship(self, itemlist):
        return
            



with open(f"ShipCase1.txt") as f:
    res1 = parse_manifest(f.read())
with open(f"ShipCase2.txt") as f:
    res2 = parse_manifest(f.read())
with open(f"ShipCase3.txt") as f:
    res3 = parse_manifest(f.read())
with open(f"ShipCase4.txt") as f:
    res4 = parse_manifest(f.read())
with open(f"ShipCase5.txt") as f:
    res5 = parse_manifest(f.read())
with open(f"SilverQueen.txt") as f:
    res6 = parse_manifest(f.read())



case1  = to_grid(res1) 
Unload_Case = Node(case1)


cat_amount = Unload_Case.item_amount("Cat")
print(cat_amount)
curr_node = Unload_Case
frontier = [curr_node]
curr_node.unload_ship(["Cat"])
while cat_amount > 0:
    curr_node.unload_ship(["Cat"])
    frontier.pop(0)
    for child in curr_node.child_nodes:
        frontier.append(child)
    curr_node = frontier[0]
    cat_amount = curr_node.item_amount("Cat")
