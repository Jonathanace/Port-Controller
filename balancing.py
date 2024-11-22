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
import sys

def can_balance(items: list["Item"]) -> bool:
    """Checks if the ship can be balanced
    
    Parameters: 
    items: list[Item]
        list of items given by parse_manifest
    
    Returns:
    bool
        True if the ship can be balanced, False if not
    """
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
        #print(sum)
        if 0.9 * sum < total_weight - sum < 1.1 * sum:
            #print("True")
            return True
    # for item in arr:
    #     currWeight += item
    #     print(currWeight, totalWeight - currWeight)
    #     if 0.9 * currWeight < totalWeight - currWeight < 1.1 * currWeight:
    #         return True
    # prefix_sum = 0
    # min_diff = sys.maxsize
    # larger = 0
    # smaller = 0
    # for i in range(len(arr)):
    #     prefix_sum += arr[i]
    #     diff = abs((total_weight - prefix_sum) - prefix_sum)
    #     print(total_weight - prefix_sum, prefix_sum, diff)
    #     if diff < min_diff:
    #         min_diff = diff
    #         larger = max(total_weight - prefix_sum, prefix_sum)
    #         smaller = min(total_weight - prefix_sum, prefix_sum)
    # if larger / smaller < 1.1:
    #     return True
    # return False
    return False

#Recursive function that checks every possible combination of container weights.
def container_combinations(arr, data, start, end, index, r, total, sums):
    if index == r:
        sum = 0
        for j in range(r):
            sum += data[j]
        #     print(data[j], end=" ")
        # print()
        # print("Sum and Difference: ", end="")
        # print(sum, total-sum)
        sums.append(sum)
        return sum
    i = start
    while i <= end and end - i + 1 >= r - index:
        data[index] = arr[i]
        container_combinations(arr, data, i + 1, end, index + 1, r, total, sums)
        i += 1

# #Recursive function to find two non-sequential subarrays with the smallest difference between them. Outputs two integers.
# def min_diff(num, sum_a, sum_b, index_a, index_b):
#     index = index_a + index_b + 2
#     if index == len(num):
#         return sum_a, sum_b
#     elif max(index_a, index_b) * 2 > len(num) - 1:
#         return sys.maxsize, 0
#     elif abs(sum_a + num[index] - sum_b) < abs(sum_b + num[index] - sum_a):
#         temp1, temp2 = min_diff(num, sum_a + num[index], sum_b, index_a + 1, index_b)
#         result = abs(temp1 - temp2)
#         if result > 0:
#             temp3, temp4 = min_diff(num, sum_b + num[index], sum_a, index_b + 1, index_a)
#             if result > abs(temp3 - temp4):
#                 return temp3, temp4
#         return temp1, temp2
#     else:
#         temp5, temp6 = min_diff(num, sum_b + num[index], sum_a, index_b + 1, index_a)
#         result = abs(temp5 - temp6)
#         if result > 0:
#             temp7, temp8 = min_diff(num, sum_a + num[index], sum_b, index_a + 1, index_b)
#             if result > abs(temp7 - temp8):
#                 return temp7, temp8
#         return temp5, temp6
    

#Main balancing function. Outputs the final goal state.
def balance(items: list["Item"]):
    res = to_grid(items)
    start = Node(res)
    if can_balance(items) == False:
        print("Can\'t be balanced")
        #SIFT Here
        return start
    frontier = [start]
    explored = []
    goal_reached = False
    # first = tuple([1, 1])
    # second = tuple([0, 3])
    # arr = swap_squares(start, first, second)
    while goal_reached == False:
        temp_frontier = []
        for state in frontier:
            curr_weight_arr = []
            temp_state = state.ship
            for q in range(len(state.ship)):
                for w in range(len(state.ship[q])):
                    curr_weight_arr.append(state.ship[q][w].weight)
            # for i in range(len(temp_state)):
            #     print("[", end="")
            #     for j in range(len(temp_state[i])):
            #         print(temp_state[i][j].weight, end=" ")
            #     print("]", end="\n")
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
                    weight_arr = []
                    for q in range(len(child_node.ship)):
                            for w in range(len(child_node.ship[q])):
                               weight_arr.append(child_node.ship[q][w].weight)
                    for explored_node in explored:
                        # if np.array_equal(child_node.ship, explored_node) == True:
                             # print("DUPLICATE")
                            # exists = True
                            # break
                        if explored_node == weight_arr:
                            exists = True
                            break
                    if exists == False or len(explored) == 0:
                        # print("Added")
                        temp_frontier.append(child_node)
            explored.append(curr_weight_arr)
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
    #max(weight(port),weight(starboard)) / min(weight(port),weight(starboard)) < 1.1
    diff = min(left, right) / max(left, right)
    if diff > 0.9:
        # print(left, right)
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

#Estimates the time it took for a container to be moved to another. Returns an integer.
def time_estimate(curr: Node, prev: Node):
    curr_ship = curr.ship
    positions = []
    if(prev == None):
        print("This is the start state")
        return positions
    prev_ship = prev.ship
    changes = 0
    while changes < 2:
        for i in range(len(curr_ship)):
            for j in range(len(curr_ship[i])):
                if curr_ship[i][j].weight != prev_ship[i][j].weight:
                    temp = curr_ship[i][j].position
                    positions.append(temp)
                    changes += 1
            #     if changes == 2:
            #         break
            # if changes == 2:
            #         break
    first_column = positions[0][1]
    second_column = positions[1][1]
    start_row = positions[0][0]
    end_row = positions[1][0]
    #print(positions)
    sum = 0
    max_height = 0
    if(first_column < second_column):
        max_height = start_row - 1
    if(second_column < first_column):
        max_height = end_row - 1
    for k in range(min(first_column, second_column), max(first_column, second_column)):
        # print(k)
        n = 7
        while n >= 0:
            if prev_ship[n][k].is_empty == False:
                #print("Column:", k)
                #print("Compare:", n + 1)
                if n + 1 > max_height:
                    max_height = n + 1
                #print("Max:", max_height)
            n -= 1
    max_height = max_height + 1
    #print("Max height:", max_height)
    sum += max_height - start_row
    # print(sum)
    sum += max_height - end_row
    # print(sum)
    sum += abs(second_column - first_column)
    # print(sum)
    return sum, positions


#Takes the output from the main balancing function and translates it into an array of step objects. Outputs the array. Intended to be used by front end, and will be the function that is called when the user selects the balancing option.
def get_balancing_steps(items: list["Item"]):
    res = []
    curr = balance(items)
    while(curr != None):
        for i in range(len(curr.ship)):
            print("[", end="")
            for j in range(len(curr.ship[i])):
                print(curr.ship[i][j].weight, end=" ")
            print("]", end="\n")
        prev = curr.previous_node
        if(prev == None):
            break
        time_estimation, positions = time_estimate(curr, prev)
        print(time_estimation)
        p = positions[0]
        x = p[0]
        y = p[1]
        start_pos = tuple([0,0])
        end_pos = tuple([0,0])
        if curr.ship[x][y].is_empty == True:
            start_pos = positions[1]
            end_pos = positions[0]
        else:
            start_pos = positions[0]
            end_pos = positions[1]
        temp = Step(start_pos, end_pos, time_estimation)
        res.append(temp)
        curr = prev
    #     print("New step")
    #     prev = curr.previous_node
  
    # print("New step")
    # arr = time_estimate(curr, prev)
    # for i in range(len(arr)):
    #         print("[", end="")
    #         for j in range(arr[i]):
    #             print(arr[i][j].weight, end=" ")
    #         print("]", end="\n")
    res.reverse()
    return res
    

with open(f"ShipCase4.txt") as f:
    import time
    start_time = time.time()
    res = parse_manifest(f.read())
    arr = get_balancing_steps(res)
    end_time = time.time()
    for square in arr:
        print(square.start_pos, square.end_pos, square.time_estimate)
    time_spent = end_time - start_time
    print(time_spent, "seconds spent")