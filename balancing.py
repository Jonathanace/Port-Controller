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

def check_balanced()

#Each step contains start pos and end pos
def balance(items: list["Item"]):
    if can_balance(items) == False:
        #SIFT Here
        return(0)
    res = to_grid(items)
    start = Node(res)
    frontier = [start.ship]
    explored = []
    steps = []
    
    return(res)

with open(f"SilverQueen.txt") as f:
    import time
    start_time = time.time()
    res = parse_manifest(f.read())
    arr = balance(res)
    end_time = time.time()
    for row in arr:
        for square in row:
            print(square.position, square.name, square.weight, square.isHull, square.isEmpty)
    time_spent = end_time - start_time
    print(time_spent, "seconds spent")