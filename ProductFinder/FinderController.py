from FinderModel import FinderModel
from FinderView import FinderView

DefaultSettings = {
    "mapSize": (5, 5),
    "rotation": 0,
    "algorithm": "BFS",
    "worker": (0, 0),
    "shelves": [(2, 3), (3, 2), (3, 4), (4, 3)]
}


class FinderController:
    def __init__(self, model: FinderModel, view: FinderView, settings: dict):
        self.model = model
        self.view = view
        self.settings = settings if settings else DefaultSettings

    def start(self):
        while True:
            choice = self.view.printMainMenu()
            if choice == "1":
                self.getProduct()
            elif choice == "2":
                self.setting()
            elif choice == "3":
                break
            else:
                print("invalid input, please try again")

    def getProduct(self):
        self.view.printMap(mapSize=self.settings['mapSize'], worker=self.settings["worker"],
                           shelves=self.settings["shelves"], path=None)

        while True:
            destination = self.view.inputDestination()

            optimal_path = self.model.getPath(self.settings['worker'], destination,
                                              self.model.CreateObstacles(mapSize=self.settings['mapSize'],
                                                                         shelves=self.settings['shelves']))
            self.view.printMap(mapSize=self.settings['mapSize'], worker=self.settings["worker"],
                               shelves=self.settings["shelves"], path=optimal_path, highlight=[destination])

            self.view.printDirection(optimal_path)

            if input("Choose one option: \n1) go get another product! \n2) back to main menu\n") == "1":
                continue
            else:
                break

    def setting(self):
        while True:
            choice = self.view.printSettingMenu()
            if choice == "1":
                self.settings['rotation'] = self.view.inputRotation()
            elif choice == "2":
                self.settings['algorithm'] = self.view.inputAlgorithm()
            elif choice == "3":
                self.settings['mapSize'] = self.view.inputMapSize()
            elif choice == "4":
                self.settings['worker'] = self.view.inputWorker()
            elif choice == "5":
                self.settings['shelves'], _ = self.view.inputShelves()
            elif choice == "6":
                self.view.printCurrentSetting(self.settings)
            elif choice == "7":
                break
            else:
                print("invalid input, please try again")
            input("press enter to continue")
