#function to check if balancing is possible
#balancing function
#Requirement:: left side weight and right side weight difference is no more than 10%
#max(weight(port),weight(starboard)) / min(weight(port),weight(starboard)) < 1.1
#Node: numpy array to represent ship grid
#Grid container
from utils import Item
from utils import parse_manifest
from states import Grid
from states import toGrid
import numpy as np

def canBalance(items: list["Item"]) -> bool:
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
def balance(items: list["Item"]): #-> output:
    if canBalance(items) == False:
        #SIFT Here
        return(0)
    res = toGrid(items)
    return(res)

with open(f"SilverQueen.txt") as f:
    res = parse_manifest(f.read())
    arr = balance(res)
    for row in arr:
        for square in row:
            print(square.position, square.name, square.weight, square.isHull, square.isEmpty)