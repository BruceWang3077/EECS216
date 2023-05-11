from FinderController import FinderController
from FinderModel import FinderModel
from FinderView import FinderView

def main():
    settings  = {
        "mapSize": (5, 5),
        "rotation": 0,
        "algorithm": "BFS",
        "worker": (0, 0),
        "shelves": [(2, 3), (3, 2), (3, 4), (4, 3)]
    }
    finderModel = FinderModel()
    finderView = FinderView()
    finderController = FinderController(finderModel, finderView, settings)
    finderController.start()

if __name__ == "__main__":
    main()