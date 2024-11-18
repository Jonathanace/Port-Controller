from utils import parse_manifest
from utils import Item
import numpy as np

class Grid:
    isHull: bool
    isEmpty: bool
    weight: int
    name: str
    position: tuple[int, int]
    def __init__(self, isHull, isEmpty, position, weight=None, name=None):
        self.isHull = isHull
        self.isEmpty = isEmpty
        self.position = position
        if isHull == False or isEmpty == False:
            self.setContainer(weight, name)
    
    def setEmpty(self):
        self.isEmpty = True
        self.weight = 0
        self.name = "UNUSED"
    
    def setContainer(self, weight, name):
        self.isHull = False
        self.isEmpty = False
        self.weight = weight
        self.name = name    

def toGrid(items: list["Item"]) -> np.array:
    grid = np.empty(0)
    for item in items:
        # print(item['location'])
        # print(item['weight'])
        # print(item['company'])
        isHull = False
        isEmpty = False
        if item['weight'] == 0:
            if item['company'] == "UNUSED":
                isEmpty = True
            if item['company'] == "NAN":
                isHull = True
        temp = Grid(isHull, isEmpty, item['location'], item['weight'], item['company'])
        grid = np.append(grid, temp)
    return grid

with open(f"SilverQueen.txt") as f:
    res = parse_manifest(f.read())
    arr = toGrid(res)
    for square in arr:
        print(square.name, square.weight)