from utils import *
from nodes import *
from step import *
import numpy as np
import copy
import sys

#Finds what the weight of either side should be once the sift operation is completed. Returns a pair of integers.
def sifted_weights(ship: Node):
    containers = all_containers(ship)
    l = 0
    r = 0
    for i in range(len(containers)):
        if i % 2 == 0:
            l += containers[i]
        else:
            r += containers[i]
    return l, r

#Finds all containers and returns an array of their weights.
def all_containers(ship: Node):
    curr = ship.ship
    containers = []
    for i in range(len(curr)):
        for j in range(len(curr[i])):
            square = curr[i][j]
            if square.is_empty == False and square.is_hull == False:
                containers.append(square.weight)
    containers.sort(reverse=True)
    return containers

#Checks if a state matches the sifted condition, outputs a boolean.
def check_sifted(ship: Node, l: int, r: int):
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
    if l == left and r == right:
        return True
    return False

# with open(f"ShipCase5.txt") as f:
#     import time
#     start_time = time.time()
#     res = parse_manifest(f.read())
#     grids = to_grid(res)
#     curr = Node(grids)
#     left, right = sifted_weights(curr)
#     end_time = time.time()
#     print(left, right)
#     time_spent = end_time - start_time
#     print(time_spent, "seconds spent")