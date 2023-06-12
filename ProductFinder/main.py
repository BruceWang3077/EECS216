#!/usr/bin/env python3
import sys

print(sys.executable)

from FinderController import FinderController
from FinderModel import FinderModel
from FinderView import FinderView


def main():
    settings = {
        "mapSize": (40, 21), # (width, height)
        "rotation": 1, # 0: 0 degree, 1: 90 degree, 2: 180 degree, 3: 270 degree (counter-clockwise)
        "algorithm": "tspDp", # "tspDp" or "branchAndBound"
        "worker": (0, 0),
        "shelves": [(2, 3), (3, 2), (3, 4), (4, 3)],
        "products": {},
        "orders": [],
        'countDown': 60 # seconds for timeout
    }
    finderModel = FinderModel()
    finderView = FinderView()
    finderController = FinderController(finderModel, finderView, settings)
    finderController.start()


if __name__ == "__main__":
    main()
