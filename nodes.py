from states import Grid 
from states import to_grid
from utils import parse_manifest
from utils import Item
from step import Step
class Node:
    def __init__(self, ship,movement = None, holding_area = None, trucks = False, previous_node = None, crane_pos = "Start", moves = None, index_on_top = None):
        self.ship = ship
        self.holding_area = holding_area
        self.trucks = trucks
        self.previous_node = previous_node
        self.child_nodes = []
        self.movement = movement

        self.crane_pos = crane_pos
        self.moves = moves
        self.index_on_top = index_on_top
        self.h = 0
        if self.moves is not None:
            self.unload_item = self.get_unload_item()
        if previous_node != None:
            self.step = self.create_step()
            self.calculate_h()
            self.calculate_h()

    
    
    def get_unload_item(self):
        unload_move = self.moves[0]
        items = []
        if unload_move is None:
            self.unload_item = None
        else:
            for unload in unload_move:
                if unload[1] > 0:
                    items.append(unload[0])
            if len(items) == 0:
                self.unload_item = None
            else:
                self.unload_item = items

    # checks if there is anything above the container, will be used in the move function
    # index [x,y]
    def check_above(self,index: tuple[int,int]) -> bool:
        if index[0] == 7:
            return True
        if self.ship[index[0] + 1][index[1]].is_empty == True:
            return True
        return False
    
    # checks which possibe spot they can move to
    #index[x,y]
    def check_available(self,index: tuple[int,int]):
        available_moves = []
        column = index[1]
        l = column - 1
        r = column + 1
        while l >= 0 or r < len(self.ship[0]):
            if l >= 0:
                left_temp = self.check_column(l)
                available_moves.append(left_temp)
                l -= 1
            if r < len(self.ship[0]):
                right_temp = self.check_column(r)
                available_moves.append(right_temp)
                r += 1
        return available_moves

    #Helper function that finds the highest empty square in a column
    def check_column(self, col: int):
        curr = self.ship
        n = 7
        res = tuple([0,0])
        while n >= 0:
            if curr[n][col].is_empty == False:
                if n + 1 < 8:
                    res = tuple([n + 1, col])
                    return res
                else:
                    return
            if n == 0:
                res = tuple([n, col])
                return res
            n -= 1
        res = tuple([n, col])
        return res

    def check_aviable_load(self):
        available_moves = []
        for j in range(len(self.ship[0])):
            available_moves.append(self.check_column(j))
        return available_moves
    def get_position(self):
        ship2 = self.ship
        ship1 = self.previous_node.ship
        for i in range(len(ship1)):
            for j in range(len(ship1[0])):
                if ship1[i][j].name != ship2[i][j].name:
                    return ship2[i][j].position, ship2[i][j].name
    def time_estimate(self):
        if self.movement == 'Load' or self.movement == 'Unload':
            time = 0
            position,name = self.get_position()
            portal = [9,1]
            x_distance = abs(position[0] - portal[0])
            y_distance = abs(position[1] - portal[1])
            time = 2 + x_distance + y_distance
            return time, position, name
        else:
            prev_ship = self.previous_node.ship
            changes = 0
            positions = []
            while changes < 2:
                for i in range(len(self.ship)):
                    for j in range(len(self.ship[i])):
                        if self.ship[i][j].weight != prev_ship[i][j].weight:
                            temp = self.ship[i][j].position
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

    def create_step(self):
        if self.movement == "Balance" or self.movement == "SIFT" or self.movement == "Move_On_Top":
            movement_type = self.movement
            time_estimation, positions = self.time_estimate()
            p = positions[0]
            x = p[0] - 1
            y = p[1] - 1
            start_pos = tuple([0,0])
            end_pos = tuple([0,0])
            if self.ship[x][y].is_empty == True:
                start_pos = positions[0]
                end_pos = positions[1]
            else:
                start_pos = positions[1]
                end_pos = positions[0]
            s1 = end_pos[0] - 1
            s2 = end_pos[1] - 1
            temp_grid = self.ship[s1][s2]
            weight = temp_grid.weight
            temp = Step(start_pos, end_pos, time_estimation, movement_type, weight = weight)
            return temp

        if self.movement == "Load":
            time_estimation, position, name = self.time_estimate()
            start_pos = "Dock"
            end_pos = position
            movement_type = self.movement
            temp = Step(start_pos, end_pos, time_estimation, movement_type, name)
            return temp
        if self.movement == "Unload":
            time_estimation, position, name = self.time_estimate()
            start_pos = position
            end_pos = "Dock"
            movement_type = self.movement
            temp = Step(start_pos, end_pos, time_estimation, movement_type)
            return temp
    def check_unload_load(self):
        if self.movement == "Unload" and self.previous_node.movement == "Load":
            return -2
        if self.movement == "Load" and self.previous_node.movement == "Unload":
            return -2
        if self.movement == "Unload" and self.previous_node.movement is None:
            if self.moves[1] is not None:
                return  len(self.moves[0]) - len(self.moves[1])
            else:
                return  0
        if self.movement == "Load" and self.previous_node.movement is None:
            if self.moves[0] is not None:
                return len(self.moves[1]) - len(self.moves[0])
            else:
                return 0
        else:
            count = 4
        return count
    def check_unload_item(self , position):
        self.get_unload_item()
        if self.unload_item is None:
            return 0
        column = position[1] - 1
        last_row = position[0] - 1
        for i in range(last_row):
            for item in self.unload_item:
                if self.ship[i][column].name == item:
                    return 2 + last_row - i
        return 0 
    def calculate_h(self):
        if self.movement == "Balance" or self.movement == "SIFT":
            curr = self.ship
            prev = self.previous_node.ship
            left = 0
            right = 0
            bal_diff = 0
            for i in range(6):
                j = i + 6
                for n in range(len(curr) - 1):
                    temp_left = curr[n][i]
                    temp_right = curr[n][j]
                    left += temp_left.weight
                    right += temp_right.weight
            h1 = abs(left - right) - bal_diff
            step = self.step
            time = step.time_estimate
            container_pos = step.start_pos
            x = container_pos[0] - 1
            y = container_pos[1] - 1
            weight_below = 1
            if(x >= 1):
                # print(container_pos)
                temp_grid = prev[x - 1][y]
                # print(temp_grid.position)
                weight_below = max(1, temp_grid.weight)
            h2 = weight_below * time
            container_columns = 0
            if(left > right):
                for i in range(6):
                    n = 7
                    while n >= 0:
                        if curr[n][i].is_empty == False and curr[n][i].is_hull == False:
                            container_columns += 1
                        n -= 1
            else:
                for i in range(6, 12):
                    n = 7
                    while n >= 0:
                        if curr[n][i].is_empty == False and curr[n][i].is_hull == False:
                            container_columns += 1
                        n -= 1
            h3 = max(left, right) / container_columns
            h_temp = h1 + h2 + h3
            self.h = h_temp / weight_below
        if self.movement == "Unload":
            h1 = self.check_unload_load()
            h2 = self.step.time_estimate
            self.h = h1 + h2 + self.previous_node.h
        if self.movement == "Load":
            h1 = self.check_unload_load()
            h2 = self.step.time_estimate
            h3 = self.check_unload_item(self.step.end_pos)
            self.h = h1 + h2 + self.previous_node.h
        if self.movement == "Move_On_Top":
            h1 = self.step.time_estimate
            start_pos = self.step.start_pos
            end_pos = self.step.end_pos
            if start_pos[1] > end_pos[1]:
                h2 = -1
            if start_pos[1] < end_pos[1]:
                h2 = 0
            h3 = self.check_unload_item(self.step.end_pos)
            self.h = h1+ h2 + h3 + self.previous_node.h

    
    def get_step(self):
        return self.step
    
    def get_h(self):
        if self.previous_node == None:
            return 0
        return self.h
    def check_aviable_load(self):
        available_moves = []
        for j in range(len(self.ship[0])):
            if self.check_column(j) is not None:
                available_moves.append(self.check_column(j))
        return available_moves

