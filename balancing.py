#function to check if balancing is possible
#balancing function
#Requirement:: left side weight and right side weight difference is no more than 10%
#max(weight(port),weight(starboard)) / min(weight(port),weight(starboard)) < 1.1
#Node: numpy array to represent ship grid
#Grid container
from utils import Item
from utils import parse_manifest
from states import Grid
from states import to_grid
from nodes import Node
from step import Step
import numpy as np
import copy

def can_balance(items: list["Item"]) -> bool:
    """Checks if the ship can be balanced
    
    Parameters: 
    items: list[Item]
        list of items given by parse_manifest
    
    Returns:
    bool
        True if the ship can be balanced, False if not
    """
    totalWeight = 0
    for item in items:
        totalWeight += item['weight']
    currWeight = 0
    for item in items:
        currWeight += item['weight']
        if 0.9 * currWeight < totalWeight - currWeight < 1.1 * currWeight:
            return True
    return False


#Each step contains start pos and end pos
def balance(items: list["Item"]):
    if can_balance(items) == False:
        #SIFT Here
        return(0)
    res = to_grid(items)
    start = Node(res)
    frontier = [start]
    explored = []
    goal_reached = False
    # first = tuple([1, 1])
    # second = tuple([0, 3])
    # arr = swap_squares(start, first, second)
    while goal_reached == False:
        temp_frontier = []
        for state in frontier:
            if is_balanced(state) == True:
                # print("Balanced")
                goal_reached = True
                return state
            movable = movable_containers(state)
            for container in movable:
                x = container[0]
                y = container[1]
                temp = tuple([x, y])
                available = state.check_available(temp)
                for a in available:
                    new_ship = swap_squares(state, temp, a)
                    child_node = Node(new_ship, previous_node=state)
                    # if child_node.ship not in explored:
                    #     temp_frontier.append(child_node)
                    exists = False
                    for explored_node in explored:
                        if np.array_equal(child_node.ship, explored_node) == True:
                            exists = True
                            break
                    if exists == False:
                        # print("Added")
                        temp_frontier.append(child_node)
            explored.append(state.ship)
        frontier = []
        for new_state in temp_frontier:
            frontier.append(new_state)
    return start

def movable_containers(ship: Node):
    curr = ship.ship
    movable = []
    for i in range(len(curr[0])):
        j = len(curr) - 1
        while j >= 0:
            if curr[j][i].is_empty == False and curr[j][i].is_hull == False:
                temp = tuple([j, i])
                if ship.check_above(temp) == True:
                    movable.append(temp)
                    break
            j -= 1
    return movable

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
    #max(weight(port),weight(starboard)) / min(weight(port),weight(starboard)) < 1.1
    diff = min(left, right) / max(left, right)
    if diff > 0.9:
        # print(left, right)
        return True
    return False

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
    

# with open(f"SilverQueen.txt") as f:
#     import time
#     start_time = time.time()
#     res = parse_manifest(f.read())
#     arr = balance(res)
#     end_time = time.time()
#     for row in arr.ship:
#         for square in row:
#             print(square.position, square.name, square.weight)
#     time_spent = end_time - start_time
#     print(time_spent, "seconds spent")