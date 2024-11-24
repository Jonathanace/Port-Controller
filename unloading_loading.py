from utils import Item
from utils import parse_manifest
from states import Grid
from states import to_grid
from nodes import Node
from step import Step
import numpy as np
import copy
import sys


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

unload = [("Cat", 1)]
# cargo = (unload[0], unload[1] -1)
# print(unload)
# print(cargo)
def calculate_goal_state(unload : list[tuple[str,int]] = None,load : list[tuple[str,int]] = None) -> list[tuple[str,int]]:
    goal_state = []
    if unload is not None:
        for cargo in unload:
            final_cargo = (cargo[0], cargo[1] - 1)
            goal_state.append(final_cargo)
    if load is not None:
        for cargo in load:
            final_cargo = (cargo[0], cargo[1] - 1)
            goal_state.append(final_cargo)

    return goal_state
print(calculate_goal_state(unload= unload))
def find_item_amount(items : list[str], ship):
    count = 0 
    for item in items:
        for i in range(len(ship)):
            for j in range(len(ship[0])):
                if ship[i][j].name == item:
                    count += 1
    return count
print(find_item_amount(["Cat"], Unload_Case.ship))




# def find_item(self, item):
#         index_list = []
#         for i in range(len(self.ship)):
#             for j in range(len(self.ship)):
#                 if self.ship[i][j].name == item:
#                     index_list.append([i,j])
#         if len(index_list) == 0:
#             return index_list
#         return index_list
# def item_amount(self, item):
#         amount = 0
#         for i in range(len(self.ship)):
#             for j in range(len(self.ship)):
#                 if self.ship[i][j].name == item:
#                     amount+=1
#         return amount
#     def unload_ship(self, itemlist):
#         #indexes for every item on the ship
#         for item in itemlist:
#             possible_indexes = self.find_item(item)
#             if len(possible_indexes) == 0:
#                 break
#             for index in possible_indexes:
#                 if self.check_above(index):
#                     #print(self.ship[index[0],index[1]].name)
#                     temp_ship = self.ship
#                     temp_ship[index[0],index[1]].set_empty()
#                     child_node = Node(temp_ship, previous_node= self)
#                     self.child_nodes.append(child_node)
#                     #print(self.ship[index[0],index[1]].name)
#                     print(f"Moved {item} off of ship from location:  {index[0] + 1} , {index[1] + 1}" )
#         return
#     def check_available_load(self):
#         available_moves = []
#         for j in range(len(self.ship[0])):
#             #rows
#             i = len(self.ship) -1 
#             while i >= 0:
#                 print(i, j, self.ship[i][j].position, self.ship[i][j].name)
#                 if self.ship[i][j].is_empty == False:
#                     print(self.ship[i][j].position, self.ship[i][j].name)
#                     available_moves.append([i+1,j])
#                     break
#                 if i == 0:
#                     print(self.ship[i][j].position, self.ship[i][j].name)
#                     available_moves.append([i,j])
#                     break
#                 i = i -1
#         return available_moves
#     def load_ship(self, itemlist):
#         return
            



