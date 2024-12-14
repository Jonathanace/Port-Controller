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
        if (10/11) * sum < total_weight - sum < 1.1 * sum:
            return True #, total_weight - sum
    return False #, total_weight - sum

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
    movement_type = "Balance"
    if can_balance(items) == False:
        needs_sift = True
        movement_type = "SIFT"
    res = to_grid(items)
    start = Node(res, movement_type)
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
                    child_node = Node(new_ship, movement_type, previous_node=state)
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
        frontier.sort(key = lambda s : (s.get_h() + s.previous_node.get_h()))
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
    if min(left, right) != 0:
        diff = max(left, right) / min(left, right)
        if diff < 1.1:
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
def to_item_list(grid):
    items: list["Item"] = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            items.append({"location": grid[i][j].position, "weight": grid[i][j].weight, "company": grid[i][j].name})
    return items

def get_steps(file_name: str):
    with open(f"{file_name}.txt") as f:
        items = parse_manifest(f.read())
    res = []
    curr, is_sifted = balance(items)
    final_node = curr
    while(curr != None):
        prev = curr.previous_node
        if(prev == None):
            break
        res.append(curr.get_step())
        curr = prev
    item_list = to_item_list(final_node.ship)
    save_modified_manifest(item_list, file_name)
    res.reverse()
    return res
    
if __name__ == "__main__":
    files = ["ShipCase1", "ShipCase2", "ShipCase3", "ShipCase4", "ShipCase5", "SilverQueen"]
    for file in files:
        print("CURRENTLY PROCESSING:", file)
        with open(file) as f:
            import time
            start_time = time.time()
            arr = get_steps(file)
            for square in arr:
                print("Operation type is \'", square.movement_type, end=" \'; ")
                print("Weight of Container:", square.weight, end=", ")
                print("Start position:", square.start_pos, end=", ")
                print("End position:", square.end_pos, end=", ")
                print("Time estimated:", square.time_estimate, end=" ")
                print("minutes")
            end_time = time.time()
            time_spent = end_time - start_time
            print(time_spent, "seconds spent finding optimal solution")
            print('\n')