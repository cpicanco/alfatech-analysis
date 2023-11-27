import numpy as np

class Range:
    def __init__(self, low, high):
        self.low = low[0]
        self.high = high[0]

    def __contains__(self, value):
        return self.low <= value <= self.high

class RangeContainer:
    def __init__(self, values):
        self.__ranges = [Range(low, high) for low, high in zip(values[:-1], values[1:])]

    def __len__(self):
        return len(self.__ranges)

    def __getitem__(self, index):
        return self.__ranges[index]