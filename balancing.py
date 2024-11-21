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
import numpy as np

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
    steps = []
    goal_reached = False
    while goal_reached == False:
        temp_frontier = []
        for state in frontier:
            movable = movable_containers(state)
            for container in movable:
                x = container.position[0] - 1
                y = container.position[1] - 1
                temp = tuple([x, y])
                available = state.check_available(temp)
                
            
    return(movable)

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
    

with open(f"SilverQueen.txt") as f:
    import time
    start_time = time.time()
    res = parse_manifest(f.read())
    arr = balance(res)
    end_time = time.time()
    for square in arr:
        print(square)
    time_spent = end_time - start_time
    print(time_spent, "seconds spent")