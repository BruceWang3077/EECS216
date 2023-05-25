#!/usr/bin/env python3
import sys

print(sys.executable)

from FinderController import FinderController
from FinderModel import FinderModel
from FinderView import FinderView


def main():
    settings = {
        "mapSize": (40, 21),
        "rotation": 1,
        "algorithm": "BFS",
        "worker": (0, 0),
        "shelves": [(2, 3), (3, 2), (3, 4), (4, 3)],
        "products": {}
    }
    finderModel = FinderModel()
    finderView = FinderView()
    finderController = FinderController(finderModel, finderView, settings)
    finderController.start()


if __name__ == "__main__":
    main()
