from utils import Item
import numpy as np

class Grid:
    is_hull: bool
    is_empty: bool
    weight: int
    name: str
    position: tuple[int, int]
    def __init__(self, is_hull, is_empty, position, weight=None, name=None):
        self.is_hull = is_hull
        self.is_empty = is_empty
        self.position = position
        if is_hull == False and is_empty == False:
            self.set_container(weight, name)
        else:
            self.weight = weight
            self.name = name
    
    def set_empty(self):
        self.is_empty = True
        self.weight = 0
        self.name = "UNUSED"
    
    def set_container(self, weight, name):
        self.is_hull = False
        self.is_empty = False
        self.weight = weight
        self.name = name    

def to_grid(items: list["Item"]) -> np.array:
    grid = np.empty((8, 12), dtype=Grid)
    for item in items:
        # print(item['location'])
        # print(item['weight'])
        # print(item['company'])
        is_hull = False
        is_empty = False
        if item['weight'] == 0:
            if item['company'] == "UNUSED":
                is_empty = True
            if item['company'] == "NAN":
                is_hull = True
        pos = item['location']
        temp = Grid(is_hull, is_empty, pos, item['weight'], item['company'])
        x = pos[0]
        y = pos[1]
        grid[x - 1, y - 1] = temp
    return grid


