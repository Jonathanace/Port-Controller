from utils import Item
from utils import parse_manifest
from states import Grid
from states import to_grid
from nodes import Node
from step import Step
from sift import *
import numpy as np
import copy
import sys

'''
IMPORTANT: If there are two Nodes who have the same heuristic value, pick the Node that moves the container further away from the center
Heuristic Ideas: Difference btwn ideal difference btwn side weights and current difference btwn side weights 
                Total time taken to make the move multiplied by the weight of the container being moved
                Weight of heavier side divided by number of columns with containers in them.
'''



#Checks if a ship can be balanced by looking through each combination of containers and seeing if any pair of sums is within 10% of each other.
def can_balance(items: list["Item"]) -> bool:
    arr = []
    total_weight = 0
    for item in items:
        total_weight += item['weight']
        if(item['weight'] != 0):
            arr.append(item['weight'])
    arr.sort()
    sums = []
    for r in range(len(arr)):
        data = [0]*r
        container_combinations(arr, data, 0, len(arr) - 1, 0, r, total_weight, sums)
    for sum in sums:
        if 0.9 * sum < total_weight - sum < 1.1 * sum:
            return True
    return False

#Recursive function that checks every possible combination of container weights.
def container_combinations(arr, data, start, end, index, r, total, sums):
    if index == r:
        sum = 0
        for j in range(r):
            sum += data[j]
        sums.append(sum)
        return sum
    i = start
    while i <= end and end - i + 1 >= r - index:
        data[index] = arr[i]
        container_combinations(arr, data, i + 1, end, index + 1, r, total, sums)
        i += 1
    
#Main balancing function. Outputs the final goal state.
def balance(items: list["Item"]):
    needs_sift = False
    if can_balance(items) == False:
        needs_sift = True
    res = to_grid(items)
    start = Node(res)
    left, right = sifted_weights(start)
    frontier = [start]
    explored = []
    goal_reached = False
    while goal_reached == False:
        temp_frontier = []
        for state in frontier:
            curr_weight_arr = []
            for q in range(len(state.ship)):
                for w in range(len(state.ship[q])):
                    curr_weight_arr.append(state.ship[q][w].weight)
            if needs_sift == True:
                if check_sifted(state, left, right) == True:
                    goal_reached = True
                    return state, needs_sift
            else:
                if is_balanced(state) == True:
                    goal_reached = True
                    return state, needs_sift
            movable = movable_centered(state)
            for container in movable:
                x = container[0]
                y = container[1]
                temp = tuple([x, y])
                available = state.check_available(temp)
                for a in available:
                    new_ship = swap_squares(state, temp, a)
                    child_node = Node(new_ship, previous_node=state)
                    exists = False
                    weight_arr = []
                    for q in range(len(child_node.ship)):
                            for w in range(len(child_node.ship[q])):
                               weight_arr.append(child_node.ship[q][w].weight)
                    for explored_node in explored:
                        if explored_node == weight_arr:
                            exists = True
                            break
                    if exists == False or len(explored) == 0:
                        temp_frontier.append(child_node)
            explored.append(curr_weight_arr)
        frontier = []
        for new_state in temp_frontier:
            frontier.append(new_state)
    return start, needs_sift

#Creates a list of containers that can be moved starting from the center of the ship. Returns an array of tuples.
def movable_centered(ship: Node):
    movable = []
    l = 4
    r = 5
    while l >= 0 or r < 12:
        if l >= 0:
            temp, exists = movable_column(ship, l)
            if exists == True:
                movable.append(temp)
            l -= 1
        if r < 12:
            temp, exists = movable_column(ship, r)
            if exists == True:
                movable.append(temp)
            r += 1
    return movable
    
#Helper function for movable_centered, checks for a movable container in a specified column. Returns a tuple of ints.
def movable_column(ship: Node, col: int):
    curr = ship.ship
    n = 7
    res = tuple([0,0])
    while n >= 0:
        if curr[n][col].is_empty == False and curr[n][col].is_hull == False:
            res = tuple([n, col])
            return res, True
        n -= 1
    return res, False

#Checks if the ship is balanced. Ouputs a boolean.
def is_balanced(ship: Node):
    curr = ship.ship
    left = 0
    right = 0
    for i in range(6):
        j = i + 6
        for n in range(len(curr) - 1):
            temp_left = curr[n][i]
            temp_right = curr[n][j]
            left += temp_left.weight
            right += temp_right.weight
    diff = min(left, right) / max(left, right)
    if diff > 0.9:
        return True
    return False

#Changes position and information of two squares on the ship. Outputs an array that has those changes.
def swap_squares(ship: Node, first_obj: tuple[int, int], second_obj: tuple[int, int]):
    curr = copy.deepcopy(ship.ship)
    temp = curr[first_obj[0]][first_obj[1]]
    curr[first_obj[0]][first_obj[1]] = curr[second_obj[0]][second_obj[1]]
    curr[second_obj[0]][second_obj[1]] = temp
    new_pos1 = tuple([first_obj[0] + 1, first_obj[1] + 1])
    new_pos2 = tuple([second_obj[0] + 1, second_obj[1] + 1])
    curr[first_obj[0]][first_obj[1]].position = new_pos1
    curr[second_obj[0]][second_obj[1]].position = new_pos2
    return curr

#Estimates the time it took for a container to be moved to another as well as the two positions involved in a step. Returns an integer and a pair of tuples.
def time_estimate(curr: Node, prev: Node):
    curr_ship = curr.ship
    positions = []
    if(prev == None):
        return positions
    prev_ship = prev.ship
    changes = 0
    start = 0
    while changes < 2:
        for i in range(len(curr_ship)):
            for j in range(len(curr_ship[i])):
                if curr_ship[i][j].weight != prev_ship[i][j].weight:
                    temp = curr_ship[i][j].position
                    positions.append(temp)
                    changes += 1
    start_node = positions[0]
    end_node = positions[1]
    first_column = start_node[1]
    second_column = end_node[1]
    start_row = start_node[0]
    end_row = end_node[0]
    max_height = max(start_row, end_row)
    for k in range(min(first_column, second_column), max(first_column, second_column) - 1):
        n = 8
        while n >= 1:
            p = n - 1
            if prev_ship[p][k].is_empty == False:
                if n + 1 > max_height:
                    max_height = n + 1
            n -= 1
    sum = 0
    sum += max_height - start_row
    sum += max_height - end_row
    sum += abs(second_column - first_column)
    return sum, positions


#Takes the output from the main balancing function and translates it into an array of step objects. Outputs the array. Intended to be used by front end, and will be the function that is called when the user selects the balancing option.
#TO DO: add container weight to each step object
def get_balancing_steps(items: list["Item"]):
    res = []
    curr, is_sifted = balance(items)
    movement_type = "Balance"
    if is_sifted == True:
        movement_type = "SIFT"
    else:
        movement_type = "Balance"
    while(curr != None):
        prev = curr.previous_node
        if(prev == None):
            break
        time_estimation, positions = time_estimate(curr, prev)
        p = positions[0]
        x = p[0] - 1
        y = p[1] - 1
        start_pos = tuple([0,0])
        end_pos = tuple([0,0])
        if curr.ship[x][y].is_empty == True:
            start_pos = positions[0]
            end_pos = positions[1]
        else:
            start_pos = positions[1]
            end_pos = positions[0]
        temp = Step(start_pos, end_pos, time_estimation, movement_type)
        res.append(temp)
        curr = prev
    res.reverse()
    return res
    
# files = ["ShipCase1.txt", "ShipCase2.txt", "ShipCase3.txt", "ShipCase4.txt", "ShipCase5.txt", "SilverQueen.txt"]
# for file in files:
#     print("CURRENTLY PROCESSING:", file)
#     with open(file) as f:
#         import time
#         start_time = time.time()
#         res = parse_manifest(f.read())
#         arr = get_balancing_steps(res)
#         for square in arr:
#             print("Operation type is \'", square.movement_type, end=" \'; ")
#             print("Start position:", square.start_pos, end=", ")
#             print("End position:", square.end_pos, end=", ")
#             print("Time estimated:", square.time_estimate, end=" ")
#             print("minutes")
#         end_time = time.time()
#         time_spent = end_time - start_time
#         print(time_spent, "seconds spent")
#         print('\n')