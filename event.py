from enum import Enum

class Kind(Enum):
    ARR = 0
    DEP1H = 1
    DEP1L = 2
    DEP2H = 3
    DEP2L = 4

class Event:
    def __init__(self, time = 0.0, kind = 0):
        self.time = time
        self.kind = kind

    def __cmp__(self, other):
        return self.time > other.time
