from enum import Enum


class OptimizationState(Enum):
    Fix = 0
    Optimize = 1
    Constrain = 2
