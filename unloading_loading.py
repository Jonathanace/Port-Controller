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
case3 = to_grid(res3) 
Case3 = Node(case3)
case4 = to_grid(res4)
Case4 = Node(case4)
case5 = to_grid(res5)
Case5 = Node(case5)
case6 = to_grid(res6)
Case6 = Node(case6)

unload = [("Cat", 1)]
# cargo = (unload[0], unload[1] -1)
# print(unload)
# print(cargo)

def find_item_amount(item : str, ship):
    count = 0 
    for i in range(len(ship)):
        for j in range(len(ship[0])):
            if ship[i][j].name == item:
                count += 1
    return count

def calculate_goal_state(ship, unload : list[tuple[str,int]] = None,load : list[tuple[str,int]] = None) -> list[tuple[str,int]]:
    goal_state = []
    #change 1 to int, change cargo to item
    if unload is not None:
        for item in unload:
            final_cargo = (item[0], find_item_amount(item[0], ship) -item[1])
            goal_state.append(final_cargo)
    if load is not None:
        for item in load:
            final_cargo = (item[0],  find_item_amount(item[0],ship) + item[1]  )
            goal_state.append(final_cargo)

    return goal_state
unload_case2 = None
load_case2 = [("Bat",1)]
print(calculate_goal_state(Case1.ship,unload))
print(calculate_goal_state(Case2.ship, unload_case2,load_case2))

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
# print("remove item above")
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
            no_item_above_node = remove_items_above(tallest_index, index, curr_node)
            temp_ship = copy.deepcopy(no_item_above_node.ship)
            temp_ship[index[0],index[1]].set_empty()
            child_node = Node(temp_ship, previous_node=no_item_above_node, crane_pos = "Dock")
            child_nodes.append(child_node)
    return child_nodes
child_node_cases = unload_item("Doe", Case4)
print(len(child_node_cases))
print(child_node_cases[0].previous_node.ship[7,4].name)
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
    weight = 851
    child_nodes= []
    count = 0
    for index in available_indexes:
         count += 1
         temp_ship = copy.deepcopy(curr_node.ship)
         temp_ship[index[0],index[1]].set_container(weight, item)
         child_node = Node(temp_ship, previous_node=curr_node, crane_pos= "Ship")
         child_nodes.append(child_node)
         if count == 3:
             break
    return child_nodes
child_nodes_case_2 = load_item("Bat",Case2)
child_node_1_case2 = child_nodes_case_2[0]
print(get_state(["Bat"], child_node_1_case2.ship))
print(child_node_1_case2.ship[3,0].name)   


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
unload = [("Cat", 1)]
load = None
# return false if two states are different true if they are the same
def check_two_ships(ship1, ship2):
    for i in range(len(ship1)):
        for j in range(len(ship1[0])):
            if ship1[i][j].name != ship2[i][j].name:
                return False
    return True
# print(check_two_ships(child_node_case1[0].ship,Case1.ship))
def unload_load(initial_node, unload : list[tuple[str,int]] = None,load : list[tuple[str,int]] = None):
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
    frontier_node = [initial_node]
    frontier_move = [[unload,load]]
    explored = []
    curr_node = initial_node
    curr_unload = unload
    curr_load = load
    count = 0
    while goal_reached == False:
        curr_state = get_state(items_moved, curr_node.ship)
        # print(f"Node {count}")
        # count = count + 1
        # print("curr_state")
        # print(curr_state)
        # print("goal_state")
        # print(goal_state)
        if check_goal_state(curr_state, goal_state) or count == 2000:
            return curr_node
        temp_frontier = []
        temp_move = []
        if curr_unload is not None:
            for i in range(len(curr_unload)):
                if curr_unload[i][1] > 0:
                    temp_unload = copy.deepcopy(curr_unload)
                    child_nodes = unload_item(curr_unload[i][0],curr_node)
                    temp_unload[i] = change_amount(temp_unload[i], "U")
                    for child_node in child_nodes:
                        temp_frontier.append(child_node)
                        temp_move.append([temp_unload,curr_load])

                else: 
                    continue
        if curr_load is not None:
            for i in range(len(curr_load)):
                if curr_load[i][1] > 0:
                    temp_load =  copy.deepcopy(curr_load)
                    child_nodes = load_item(curr_load[i][0],curr_node)
                    temp_load[i] = change_amount(temp_load[i], "L")
                    for child_node in child_nodes:
                        temp_frontier.append(child_node)
                        temp_move.append([curr_unload,temp_load])
                else: 
                    continue
        explored.append(curr_node)
        for explored_node in explored:
            for i in range(len(temp_frontier)):
                if check_two_ships(explored_node.ship,temp_frontier[i].ship) == False:
                    frontier_node.append(temp_frontier[i])
                    frontier_move.append(temp_move[i])
                    
        frontier_node.pop(0)
        frontier_move.pop(0)
        curr_node = frontier_node[0]
        curr_unload = frontier_move[0][0]
        curr_load = frontier_move[0][1]
# print(load)
final_node_case_1 = unload_load(Case1,unload)
# print(Case1.ship[0,1].name)
# print(final_node_case_1.ship[0,1].name)
# print(final_node_case_1.previous_node.ship[0,1].name)
unload_case2 = None
load_case2 = [("Bat",1)]
final_node_case_2 = unload_load(Case2, load= load_case2)
# print(Case2.ship[2,0].name)
# print(final_node_case_2.ship[2,0].name)
# print(final_node_case_2.ship[3,0].name)
unload_case3 = [("Cow",1)]
load_case3 = [("Bat",1), ("Rat",1)]
final_node_case_3 = unload_load(Case3, unload_case3, load_case3)

unload_case3 = [("Cow",1)]
load_case3 = [("Bat",1)]


def get_all_the_nodes(goal_node):
    curr_node = goal_node
    nodes = []
    while curr_node != None:
        nodes.append(curr_node)
        curr_node = curr_node.previous_node
    nodes.reverse()
    return nodes
nodes = get_all_the_nodes(final_node_case_1)
nodes2 = get_all_the_nodes(final_node_case_2)
nodes3 = get_all_the_nodes(final_node_case_3)
print(len(nodes3))

def get_position_moved(ship1, ship2):
    indexes = []
    for i in range(len(ship1)):
        for j in range(len(ship1[0])):
            if ship1[i][j].name != ship2[i][j].name:
                indexes.append([i,j])
    return indexes

#unloading and loading

def get_time(index1, index2):
    time = 0 
    if type(index1) != str and type(index2) != str:
        x_distance = abs(index1[0] - index2[0])
        y_distance = abs(index1[1] - index2[1])
        time = x_distance + y_distance
    else:
        portal = [0,9]
        portal_time = 2
        if type(index1) == str:
            x_distance = abs(index2[0] - portal[0])
            y_distance = abs(index2[1] - portal[1])
        else:
            x_distance = abs(index1[0] - portal[0])
            y_distance = abs(index1[1] - portal[1])
        time = x_distance + y_distance + portal_time
    return time
print("time test")
print(get_time([0,8], [1,1]))
print(get_time("Dock", [0,0]))
print(get_time([0,0], "dock"))

def move_first(ship1, pos_moved):
    start_pos = []
    for i in range(pos_moved):
        if ship1[pos_moved[i][0], pos_moved[i][1]].isEmpty == False:
            start_pos = [pos_moved[i][0],pos_moved[i][1]]
            return start_pos, i 



def get_steps(nodes_list):
    steps = []
    current_pos = [0,9]
    for i in range(1, len(nodes_list)):
        print(nodes_list[i].crane_pos)
        pos_moved = get_position_moved(nodes_list[i-1].ship, nodes_list[i].ship)
        if len(pos_moved) == 2:
            first_move_pos , first_move_index  = move_first(nodes_list[i-1].ship, pos_moved[0])
            
            break
        else:
            if nodes_list[i].crane_pos == "Dock":
                # step1 = Step(current_pos, pos_moved[0], get_time(current_pos,pos_moved[0]), "Unloading" )
                # steps.append(step1)
                # current_pos = pos_moved[0]
                step = Step(current_pos, "Dock", get_time(current_pos,"Dock"), "Unloading" )
                steps.append(step)
                current_pos = "Dock"
                continue
            if nodes_list[i].crane_pos == "Ship":
                if current_pos == "Dock":
                    step1 = Step(current_pos, pos_moved[0], get_time(current_pos,  pos_moved[0]), "Loading")
                    steps.append(step1)
                    current_pos = pos_moved[0]
                    continue    
                # else: 
                #     step1 = Step(current_pos, "Dock", get_time(current_pos, "Dock"), "Loading")
                #     steps.append(step1)
                #     current_pos = "Dock"
                #     step2 = Step(current_pos, pos_moved[0], get_time(current_pos,  pos_moved[0]), "Loading")
                #     steps.append(step2)
                #     continue
                
    
        # if nodes[i+1].crane_pos == "Dock":
        #     start_pos = get_position_moved(nodes[i].ship,nodes[i+1].ship)
        #     step = Step(start_pos, "Dock", 10, "Unloading" )
        #     steps.append(step)
        # if nodes[i].crane_pos == "Dock" and nodes[i+1].crane_pos == "Ship":
        #     end_pos = get_position_moved(nodes[i].ship,nodes[i+1].ship)
        #     step = Step("Dock", end_pos, 10, "Loading")
    return steps
steps = get_steps(nodes)
steps2 = get_steps(nodes2)
print("node 3")
steps3 = get_steps(nodes3)
# # print(len(steps))
def output_step(steps):
    for step in steps:
        print(f"Start position: {step.start_pos} , end position: {step.end_pos} , time: {step.time_estimate} minutes, movement : {step.movement_type}")
output_step(steps)
output_step(steps2)