from step import Step

class Node:
    step: Step
    movement: str
    h: int
    def __init__(self, ship, movement, holding_area = None, trucks = False, previous_node = None):
        self.ship = ship
        self.holding_area = holding_area
        self.trucks = trucks
        self.previous_node = previous_node
        self.child_nodes = []
        self.movement = movement
        if previous_node != None:
            self.step = self.create_step()
            self.calculate_h()
    
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
            if n == 0:
                res = tuple([n, col])
                return res
            n -= 1
        res = tuple([n, col])
        return res

    def time_estimate(self):
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
        if self.movement == "Balance" or self.movement == "SIFT":
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
            temp = Step(start_pos, end_pos, time_estimation, movement_type, weight)
            return temp

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
            # h4 = 0
            # if(h_prev != 0):
            #     h4 = abs(h_temp - h_prev)
            # h = h1
            # h += h2
            # h += h3
            # h -= h4
            # self.h = h
            self.h = h_temp / weight_below
    
    def get_step(self):
        return self.step
    
    def get_h(self):
        if self.previous_node == None:
            return 0
        return self.h