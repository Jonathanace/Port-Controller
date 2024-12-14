from utils import Item
from utils import parse_manifest
from utils import save_modified_manifest
from states import Grid
from states import to_grid
from nodes import Node
from step import Step
import numpy as np
import copy
import sys
import os

# find the amount of each item
def find_item_amount(item : str, ship):
    count = 0 
    for i in range(len(ship)):
        for j in range(len(ship[0])):
            if ship[i][j].name == item:
                count += 1
    return count
# calcuates the goal state
def calculate_goal_state(ship, unload : list[tuple[str,int]] = None,load : list[tuple[str,int]] = None) -> list[tuple[str,int]]:
    goal_state = []
    #subtracts one from current state if unload, adds one if load
    if unload is not None:
        for item in unload:
            final_cargo = (item[0], find_item_amount(item[0], ship) -item[1])
            goal_state.append(final_cargo)
    if load is not None:
        for item in load:
            final_cargo = (item[0],  find_item_amount(item[0],ship) + item[1]  )
            goal_state.append(final_cargo)

    return goal_state

# get the current state
def get_state(items_moved : list[str] , ship):
    state = []
    for item in items_moved:
        item_count = find_item_amount(item, ship)
        cargo = (item, item_count)
        state.append(cargo)
    return state
# get each item index
def get_item_index(item,ship):
    index_list = []
    for i in range(len(ship)):
        for j in range(len(ship)):
            if ship[i][j].name == item:
                    index_list.append([i,j])
    return index_list

# finds the talles object on top of an item
def find_tallest_index(index,ship):
    tallest_index = [0,0]
    for i in range(len(ship)-1, index[0], -1):
        if ship[i][index[1]].is_empty == False:
            tallest_index = [i,index[1]]     
    return tallest_index

# swaps to items
def swap_items(index1, index2, ship):
    temp = ship[index1[0],index1[1]]
    ship[index2[0],index2[1]].set_container(temp.weight,temp.name)
    ship[index1[0],index1[1]].set_empty()
    return ship


# removes the items above already gets the most opitimal way
def remove_items_above(tallest_index, target_index, curr_node, curr_move):
    curr_index = tallest_index
    frontier = [curr_node]
    goal_reached = False
    while goal_reached == False: 
        if curr_index[0] ==  target_index[0]:
            goal_reached == True
            return curr_node
        available_indexes = curr_node.check_available(curr_index)
        for index in available_indexes:
            temp_ship = copy.deepcopy(curr_node.ship)
            temp_ship = swap_items(curr_index,index,temp_ship)
            child_node = Node(temp_ship, previous_node=curr_node, crane_pos= "Ship", movement= "Move_On_Top", moves= curr_move , index_on_top= [curr_index[0]-1, curr_index[1]])
            frontier.append(child_node)
        frontier.pop(0)
        frontier.sort(key = lambda s: (s.get_h()))
        curr_node = frontier[0]
        curr_index = frontier[0].index_on_top

# unloads the item 2 cases
def unload_item(item,curr_node, curr_move):
    child_nodes = []
    index_list = get_item_index(item, curr_node.ship)
    for index in index_list:
        if curr_node.check_above((index[0],index[1])):
            temp_ship = copy.deepcopy(curr_node.ship)
            temp_ship[index[0],index[1]].set_empty()
            child_node = Node(temp_ship, previous_node=curr_node, crane_pos = "Dock", movement= "Unload", moves = curr_move)
            child_nodes.append(child_node)
        else:
            tallest_index = find_tallest_index(index, curr_node.ship)
            no_item_above_node = remove_items_above(tallest_index, index, curr_node, curr_move)
            temp_ship = copy.deepcopy(no_item_above_node.ship)
            temp_ship[index[0],index[1]].set_empty()
            child_node = Node(temp_ship, previous_node=no_item_above_node, crane_pos = "Ship", movement = "Unload", moves= curr_move)
            child_nodes.append(child_node)
    return child_nodes
#loads item one case
def load_item(item, weight, curr_node, curr_move):
    available_indexes = curr_node.check_aviable_load()
    child_nodes= []
    # count = 0
    for index in available_indexes:
        #  count += 1
         temp_ship = copy.deepcopy(curr_node.ship)
         temp_ship[index[0],index[1]].set_container(weight, item)
         child_node = Node(temp_ship, previous_node=curr_node, crane_pos= "Ship", movement= "Load", moves = curr_move)
         child_nodes.append(child_node)
         # remove the count variable when actually testing it
        #  if count == 1:
        #      break
    return child_nodes


def check_goal_state(curr_state,goal_state):
    for i in range(len(curr_state)):
        if curr_state[i] != goal_state[i]:
            return False
    return True
def change_amount(item : tuple[str,int] , movement ):
    temp_item = list(item)
    if movement == "L":
        temp_item[1] -= 1
        item = tuple(temp_item)
    if movement == "U":
        temp_item[1] -= 1
        item = tuple(temp_item)

    return item

# return false if two states are different true if they are the same
def check_two_ships(ship1, ship2):
    for i in range(len(ship1)):
        for j in range(len(ship1[0])):
            if ship1[i][j].name != ship2[i][j].name:
                return False
    return True
def print_out_ship(ship):
    ship = ship[::-1]
    for row in ship:
        print(' '.join(obj.name for obj in row))
# unload and load main search algorithm
def unload_load(initial_node, h, unload : list[tuple[str,int]] = None,load : list[tuple[str,int]] = None):
    goal_state = calculate_goal_state(initial_node.ship, unload, load)
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
    frontier = [initial_node]
    explored = []
    curr_node = initial_node
    curr_unload = unload
    curr_load = load
    while goal_reached == False:
        curr_state = get_state(items_moved, curr_node.ship)
        if check_goal_state(curr_state, goal_state):
            return curr_node
        temp_frontier = []
        temp_move = []
        if curr_unload is not None:
            for i in range(len(curr_unload)):
                if curr_unload[i][1] > 0:
                    temp_unload = copy.deepcopy(curr_unload)
                    temp_unload[i] = change_amount(temp_unload[i], "U")
                    child_nodes = unload_item(curr_unload[i][0], curr_node, [temp_unload,curr_load])
                    for child_node in child_nodes:
                        temp_frontier.append(child_node)
                        temp_move.append([temp_unload,curr_load])
                else: 
                    continue
        if curr_load is not None:
            for i in range(len(curr_load)):
                if curr_load[i][1] > 0:
                    temp_load =  copy.deepcopy(curr_load)
                    temp_load[i] = change_amount(temp_load[i], "L")
                    child_nodes = load_item(curr_load[i][0],curr_load[i][2], curr_node , [curr_unload,temp_load])
                    for child_node in child_nodes:
                        temp_frontier.append(child_node)
                        temp_move.append([curr_unload,temp_load])
                else: 
                    continue
        explored.append(curr_node)
        remove_index = []
        for i in range(len(temp_frontier)):
            for explored_node in explored:
                if check_two_ships(explored_node.ship,temp_frontier[i].ship) == True:
                    remove_index.append(i)
                    break
        if len(remove_index) != 0:
            remove_index.sort(reverse=True)
            for index in remove_index:
                temp_frontier.pop(index)
        for node in temp_frontier:
                frontier.append(node)
        frontier.pop(0)
        if h == True:
            frontier.sort(key = lambda s: (s.get_h()))
        curr_node = frontier[0]
        curr_unload = frontier[0].moves[0]
        curr_load = frontier[0].moves[1]
# gets all the nodes
def get_all_the_nodes(goal_node):
    curr_node = goal_node
    nodes = []
    while curr_node != None:
        nodes.append(curr_node)
        curr_node = curr_node.previous_node
    nodes.reverse()
    return nodes
# output stpes
def output_steps(steps):
    for step in steps:
        if step.movement_type == 'Load':
            print(f"Operation type is {step.movement_type}; Start position {step.start_pos}, End position {step.end_pos}, Time estimated:{step.time_estimate}, Item name: {step.name}")
        else:
            print(f"Operation type is {step.movement_type}; Start position {step.start_pos}, End position {step.end_pos}, Time estimated:{step.time_estimate}")
    #     print(f"Operation type is {node_list[i].step.movement_type}; Start position {node_list[i].step.start_pos}, End position {node_list[i].step.end_pos}, Time estimated:{node_list[i].step.time_estimate}")

    # return steps
def to_item_list(grid):
    items: list["Item"] = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            items.append({"location": grid[i][j].position, "weight": grid[i][j].weight, "company": grid[i][j].name})
    return items

def get_steps(file_path, file_name, unload, load , h):
    with open(file_path) as f:
        res = parse_manifest(f.read())
    start_ship  = to_grid(res) 
    Start_Node = Node(start_ship)
    final_node = unload_load(Start_Node, h ,unload, load)
    node_list = get_all_the_nodes(final_node)
    steps = []
    for i in range(1, len(node_list)):
        steps.append(node_list[i].step)
    # output_steps(steps)
    item_list = to_item_list(final_node.ship)
    # for item in item_list:
    #     print(item)

    save_modified_manifest(item_list, file_name.replace(".txt", ""))
    return steps

if __name__ == "__main__":
    files = ["test_manifests/ShipCase1.txt", "test_manifests/ShipCase2.txt", "test_manifests/ShipCase3.txt", "test_manifests/ShipCase4.txt", "test_manifests/ShipCase5.txt", "test_manifests/SilverQueen.txt"]
    unload_cases = [[("Cat", 1)], None,  [("Cow",1)], [("Doe",1)] ,  [("Hen",1), ("Pig",1)], [("Batons",1), ("Catfish",1)] ]
    load_cases = [None ,  [("Bat",1, 431)],  [("Bat",1, 532), ("Rat",1, 6317)], [("Nat",1, 2543)] , [("Nat",1, 153),("Rat",1,2321)] , [("Nat",1,2543)]] 
    for i in range(len(files)):
        print("CURRENTLY PROCESSING:", files[i])
        with open(files[i]) as f:
            import time
            print("no huestic")
            start_time = time.time()
            steps = get_steps(files[i], unload_cases[i], load_cases[i],False)
            end_time = time.time()
            time_spent = end_time - start_time
            print(time_spent, "seconds spent")
            print('\n')
    for i in range(len(files)):
        print("CURRENTLY PROCESSING:", files[i])
        with open(files[i]) as f:
            import time
            print("huestic")
            start_time = time.time()
            steps = get_steps(files[i], unload_cases[i], load_cases[i],True)
            end_time = time.time()
            time_spent = end_time - start_time
            print(time_spent, "seconds spent")
            print('\n')
        
