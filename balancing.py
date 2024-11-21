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
                print("Balanced")
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
                        print("Added")
                        temp_frontier.append(child_node)
            ex