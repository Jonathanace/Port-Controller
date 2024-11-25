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
Case1 = Node(case1)
case2  = to_grid(res2) 
Case2 = Node(case2)

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
# print(calculate_goal_state(unload, None))
def find_item_amount(item : str, ship):
    count = 0 
    for i in range(len(ship)):
        for j in range(len(ship[0])):
            if ship[i][j].name == item:
                count += 1
    return count
# print(find_item_amount("Cat", Case1.ship))

# gets the initial state of the ship 
# returns an array of tuples containing the items, and the current amount of each item
def get_initial_state(items_moved : list[str] , ship):
    initial_state = []
    for item in items_moved:
        item_count = find_item_amount(item, ship)
        cargo = (item, item_count)
        initial_state.append(cargo)
    return initial_state
# print(get_initial_state(["Cat"], Case1.ship))

#gets the index of an item on the ship
def get_item_index(item,ship):
    index_list = []
    for i in range(len(ship)):
        for j in range(len(ship)):
            if ship[i][j].name == item:
                    index_list.append([i,j])
    return index_list
# print(get_item_index("Cat", Case1.ship))

# returns a list of child nodes
def unload_item(item,initial_node):
    child_nodes = []
    index_list = get_item_index(item, initial_node.ship)
    for index in index_list:
        if initial_node.check_above((index[0],index[1])):
            temp_ship = copy.deepcopy(initial_node.ship)
            temp_ship[index[0],index[1]].set_empty()
            child_node = Node(temp_ship, previous_node=initial_node)
            child_nodes.append(child_node)
    return child_nodes
child_node_case1 = unload_item("Cat", Case1)
print(child_node_case1[0].ship[0,1].name)
print(len(Case1.ship))
print(len(Case1.ship[0]))
# temp_ship = copy.deepcopy(Case1.ship)
# temp_ship[0,1].set_empty()
# child_Node = Node(temp_ship, previous_node= Case1)
# print(child_Node.ship[0,1].name)
# print(Case2.check_aviable_load())
def load_item(item,initial_node):
    available_indexes = initial_node.check_aviable_load()
    weight = int(input("Weight of item:"))
    child_nodes= []
    for index in available_indexes:
         temp_ship = copy.deepcopy(initial_node.ship)
         temp_ship[index[0],index[1]].set_container(weight, item)
         child_node = Node(temp_ship, previous_node=initial_node)
         child_nodes.append(child_node)
    return child_nodes
# child_nodes_case_2 = load_item("Bat",Case2)
# child_node_1_case2 = child_nodes_case_2[0]
# print(child_node_1_case2.ship[3,0].name)   


def check_goal_state(curr_state,goal_state):
    for i in range(len(curr_state)):
        if curr_state[i] != goal_state[i]:
            return False
    return True
unload = [("Cat", 1)]
load = None
case1_initial_state = get_initial_state(["Cat"], Case1.ship)
case1_goal_state = calculate_goal_state(unload, load)
# print(case1_initial_state)
# print(case1_goal_state)
# print(check_goal_state(case1_initial_state,case1_goal_state ))
# print(check_goal_state(case1_goal_state,case1_goal_state ))
def unload_load(initial_node, unload : list[tuple[str,int]] = None,load : list[tuple[str,int]] = None):
    goal_state = calculate_goal_state(unload, load)
    items_moved = []
    if unload is not None:
        for item in unload:
            items_moved.append(item[0])
    if load is not None:
        for item in load:
            items_moved.append(item[0])
            
    initial_state = get_initial_state(items_moved, Case1.ship)
    print(initial_state)
    print(goal_state)
    goal_reached = False
    frontier = [initial_node]
    explored = []
    curr_node = initial_node
    while goal_reached == False:
        temp_frontier = []
unload_load(Case1, unload)
