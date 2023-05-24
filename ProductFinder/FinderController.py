# Import the FinderModel and FinderView classes.
from FinderModel import FinderModel
from FinderView import FinderView

# Define the default settings.
DefaultSettings = {
    "mapSize": (5, 5),
    "rotation": 1,
    "algorithm": "BFS",
    "worker": (0, 0),
    "shelves": [(2, 3), (3, 2), (3, 4), (4, 3)]
}


# The FinderController class is responsible for controlling the flow of the program.
class FinderController:
    def __init__(self, model: FinderModel, view: FinderView, settings: dict):
        # Initialize the model, view, and settings.
        self.model = model
        self.view = view
        self.settings = settings if settings else DefaultSettings

    def start(self):
        # This method is called when the program starts.
        # It displays the main menu and waits for the user to select an option.
        while True:
            choice = self.view.printMainMenu()
            if choice == "1":
                # The user wants to get a product.
                self.getProduct()
            elif choice == "2":
                # The user wants to change the settings.
                self.setting()
            elif choice == "3":
                # The user wants to quit the program.
                break
            else:
                # Invalid input.
                print("invalid input, please try again")

    def getProduct(self):
        # This method is called when the user wants to get a product.
        # It prints the map, asks the user for a destination, and finds the optimal path to the destination.
        self.view.printMap(mapSize=self.settings['mapSize'], worker=self.settings["worker"],
                           shelves=self.settings["shelves"], path=None, rotation=self.settings['rotation'])

        while True:
            destination = self.view.inputDestination()

            # Find the optimal path to the destination.
            optimal_path = self.model.getPath(self.settings['worker'], destination,
                                              self.model.CreateObstacles(mapSize=self.settings['mapSize'],
                                                                         shelves=self.settings['shelves']))

            # Print the map with the optimal path highlighted.
            self.view.printMap(mapSize=self.settings['mapSize'], worker=self.settings["worker"],
                               shelves=self.settings["shelves"], path=optimal_path, highlight=[destination], rotation=self.settings['rotation'])

            # Print the directions for the optimal path.
            self.view.printDirection(path=optimal_path, rotation=self.settings['rotation'], mapSize=self.settings['mapSize'])

            # Ask the user if they want to get another product.
            if input("Choose one option: \n1) go get another product! \n2) back to main menu\n") == "1":
                continue
            else:
                break

    def setting(self):
        # This method is called when the user wants to change the settings.
        # It displays the settings menu and waits for the user to select an option.
        while True:
            choice = self.view.printSettingMenu()
            if choice == "1":
                # The user wants to change the rotation.
                self.settings['rotation'] = self.view.inputRotation()
            elif choice == "2":
                # The user wants to change the algorithm.
                self.settings['algorithm'] = self.view.inputAlgorithm()
            elif choice == "3":
                # The user wants to change the map size.
                self.settings['mapSize'] = self.view.inputMapSize()
            elif choice == "4":
                # The user wants to change the worker position.
                self.settings['worker'] = self.view.inputWorker()
            elif choice == "5":
                # The user wants to change the shelves.
                self.settings['shelves'], _ = self.view.inputShelves()
            elif choice == "6":
                # Print the current settings.
                self.view.printCurrentSetting(self.settings)
            elif choice == "7":
                # The user wants to go back to the main menu.
                break
            else:
                # Invalid input.
                print("invalid input, please try again")
            input("press enter to continue")
