class Step:
    start_pos: tuple[int, int]
    end_pos: tuple[int, int]
    time_estimate: int
    def __init__(self, start_pos, end_pos, time_estimate, movement_type, weight = None):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.time_estimate = time_estimate
        self.movement_type = movement_type
        self.weight = weight