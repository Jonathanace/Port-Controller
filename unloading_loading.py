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
case4 = to_grid(res4)
Case4 = Node(case4)

unload = [("Cat", 1)]
# cargo = (unload[0], unload[1] -1)
# print(unload)
# print(cargo)
def calculate_goal_state(unload : list[tuple[str,int]] = None,load : list[tuple[str,int]] = None) -> list[tuple[str,int]]:
    goal_state = []
    #change 1 to int, change cargo to item
    if unload is not None:
        for cargo in unload:
            final_cargo = (cargo[0], cargo[1] - 1)
            goal_state.append(final_cargo)
    if load is not None:
        for cargo in load:
            final_cargo = (cargo[0], cargo[1] - 1)
            goal_state.append(final_cargo)

    return goal_state
#print(calculate_goal_state(unload, None))
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
def get_state(items_moved : list[str] , ship):
    state = []
    for item in items_moved:
        item_count = find_item_amount(item, ship)
        cargo = (item, item_count)
        state.append(cargo)
    return state
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
# print(get_item_index("Doe", Case4.ship))
# print(Case4.ship[7,4].name)
# print(Case4.ship[6,4].name)
def find_tallest_index(index,ship):
    tallest_index = [0,0]
    for i in range(len(ship)-1, index[0], -1):
        if ship[i][index[1]].is_empty == False:
            tallest_index = [i,index[1]]     
    return tallest_index
# print(find_tallest_index([6,4],Case4.ship))
# print(Case4.ship[6,4].weight)
# returns a list of child nodes
# index1 = [7,4]
# index2 = (1,3)
# swapEx = Case4.ship

def swap_items(index1, index2, ship):
    temp = ship[index1[0],index1[1]]
    ship[index2[0],index2[1]].set_container(temp.weight,temp.name)
    ship[index1[0],index1[1]].set_empty()
    return ship
# swapEx = swap_items(index1,index2,swapEx)
# print(swapEx[1,3].name)
# print(swapEx[7,4].name)


def remove_items_above(tallest_index, target_index, curr_node):
    curr_index = tallest_index
    frontier_node = [curr_node]
    frontier_indexes= [curr_index]
    goal_reached = False
    while goal_reached == False: 
        if curr_index[0] ==  target_index[0]:
            goal_reached == True
            return curr_node
        available_indexes = curr_node.check_aviable_load()
        for index in available_indexes:
            temp_ship = copy.deepcopy(curr_node.ship)
            temp_ship = swap_items(curr_index,index,temp_ship)
            child_node = Node(temp_ship, previous_node=curr_node, crane_pos= "Ship")
            frontier_node.append(child_node)
            child_index = [curr_index[0]-1, curr_index[1]]
            frontier_indexes.append(child_index)
        frontier_node.pop(0)
        frontier_indexes.pop(0)
        curr_node = frontier_node[0]
        curr_index = frontier_indexes[0]

# test_node = remove_items_above([7,4], [6,4], Case4)
# print(test_node.ship[7,4].name)
# print(test_node.ship[6,4].name)


def unload_item(item,curr_node):
    child_nodes = []
    index_list = get_item_index(item, curr_node.ship)
    for index in index_list:
        if curr_node.check_above((index[0],index[1])):
            temp_ship = copy.deepcopy(curr_node.ship)
            temp_ship[index[0],index[1]].set_empty()
            child_node = Node(temp_ship, previous_node=curr_node, crane_pos = "Dock")
            child_nodes.append(child_node)
        else:
            tallest_index = find_tallest_index(index, curr_node.ship)
            child_node = remove_items_above(tallest_index, index, curr_node)
    return child_nodes
# child_node_case1 = unload_item("Cat", Case1)
# print(child_node_case1[0].ship[0,1].name)
# print(len(Case1.ship))
# print(len(Case1.ship[0]))
# temp_ship = copy.deepcopy(Case1.ship)
# temp_ship[0,1].set_empty()
# child_Node = Node(temp_ship, previous_node= Case1)
# print(child_Node.ship[0,1].name)
# print(Case2.check_aviable_load())
def load_item(item,curr_node):
    available_indexes = curr_node.check_aviable_load()
    weight = int(input("Weight of item:"))
    child_nodes= []
    for index in available_indexes:
         temp_ship = copy.deepcopy(curr_node.ship)
         temp_ship[index[0],index[1]].set_container(weight, item)
         child_node = Node(temp_ship, previous_node=curr_node, crane_pos= "Ship")
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
def change_amount(item : tuple[str,int] , movement ):
    temp_item = list(item)
    if movement == "L":
        temp_item[1] += 1
        item = tuple(temp_item)
    if movement == "U":
        temp_item[1] -= 1
        item = tuple(temp_item)

    return item
unload = [("Cat", 1)]
load = None
# for i in range(len(unload)):
#     if unload[i][1] > 0:
#         child_nodes = unload_item(unload[i],Case1)
#         unload[i] = change_amount(unload[i], "U")
#     else: 
#         continue
# for item in unload:
#     if item[1] > 0:
#         child_nodes = unload_item(item, Case1)
#         item = change_amount(item , "U")
#         print()
#     else:
#         continue
# print(unload)
# case1_initial_state = get_state(["Cat"], Case1.ship)
# case1_goal_state = calculate_goal_state(unload, load)
# # print(case1_initial_state)
# print(case1_goal_state)
# print(check_goal_state(case1_initial_state,case1_goal_state ))
# print(check_goal_state(case1_goal_state,case1_goal_state ))

# return false if two states are different true if they are the same
def check_two_ships(ship1, ship2):
    for i in range(len(ship1)):
        for j in range(len(ship1[0])):
            if ship1[i][j].name != ship2[i][j].name:
                return False
    return True
# print(check_two_ships(child_node_case1[0].ship,Case1.ship))
def unload_load(initial_node, unload : list[tuple[str,int]] = None,load : list[tuple[str,int]] = None):
    goal_state = calculate_goal_state(unload, load)
    items_moved = []
    unload_items = []
    load_items = []
    if unload is not None:
        for item in unload:
            items_moved.append(item[0])
            unload_items.append(item[0])
    if load is not None:
        for item in load:
            items_moved.append(item[0])
            load_items.append(item[0])     
    goal_reached = False
    frontier_node = [initial_node]
    frontier_move = []
    explored = []
    curr_node = initial_node
    curr_unload = unload
    curr_load = load
    while goal_reached == False:
        curr_state = get_state(items_moved, curr_node.ship)
        if check_goal_state(curr_state, goal_state):
            return curr_node
        temp_frontier = []
        if curr_unload is not None:
            for i in range(len(unload)):
                if unload[i][1] > 0:
                    child_nodes = unload_item(unload[i][0],Case1)
                    unload[i] = change_amount(unload[i], "U")
                    for child_node in child_nodes:
                        temp_frontier.append(child_node)
                else: 
                    continue
        if curr_load is not None:
            for item in range(len(load)):
                if load[i][1] > 0:
                    child_nodes = unload_item(load[i],Case1)
                    unload[i] = change_amount(unload[i], "L")
                    for child_node in child_nodes:
                        temp_frontier.append(child_node)
                else: 
                    continue
        explored.append(curr_node)
        for explored_node in explored:
            for temp_node in temp_frontier:
                if check_two_ships(explored_node.ship,temp_node.ship) == False:
                    frontier_node.append(temp_node)
        frontier_node.pop(0)
        curr_node = frontier[0]
final_node = unload_load(Case1,unload)
print(Case1.ship[0,1].name)
print(final_node.ship[0,1].name)
print(final_node.previous_node.ship[0,1].name)