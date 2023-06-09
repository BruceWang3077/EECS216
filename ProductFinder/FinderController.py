# Import the FinderModel and FinderView classes.
from FinderModel import FinderModel
from FinderView import FinderView

from memory_profiler import memory_usage
import time


# The FinderController class is responsible for controlling the flow of the program.
class FinderController:
    def __init__(self, model: FinderModel, view: FinderView, settings: dict):
        # Initialize the model, view, and settings.
        self.model = model
        self.view = view
        self.settings = settings

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
                self.test()
            elif choice == "4":
                # The user wants to quit the program.
                break
            else:
                # Invalid input.
                print("invalid input, please try again")

    def test(self):
        if (len(self.settings['shelves']) < 5):
            print("please import warehouse data first!")
            return
        test_cases = [[108335], [108335, 391825, 340367, 286457, 661741],
                      [281610, 342706, 111873, 198029, 366109, 287261, 76283, 254489, 258540, 286457],
                      [427230, 372539, 396879, 391680, 208660, 105912, 332555, 227534, 68048, 188856, 736830, 736831,
                       479020, 103313, 1],
                      [633, 1321, 3401, 5329, 10438, 372539, 396879, 16880, 208660, 105912, 332555, 227534, 68048,
                       188856, 736830, 736831, 479020, 103313, 1, 20373]]
        print("Test cases: ", test_cases)
        if input('Make sure the settings is correct before testing. y/n?') == 'y':
            for algo in ['tspDp', 'branchAndBound']:
                self.settings['algorithm'] = algo
                for test_case in test_cases:
                    destination_list = []
                    for ID in test_case:
                        destination_list.append(self.settings['products'][str(ID)])
                    print("Destination list: ", destination_list)

                    # Start the timer and memory usage tracker.
                    start_time = time.time()
                    #mem_usage_before = memory_usage(-1, interval=0.1, timeout=1)[0]

                    def memory_test():
                        return self.model.get_optimal_path(self.settings, destination_list)

                    mem_usage = memory_usage(memory_test)
                    max_mem_usage = max(mem_usage)
                    # Find the optimal path.
                    optimal_path = memory_test();
                    #mem_usage_after = memory_usage((self.model.get_optimal_path,), -1, interval=0.1, timeout=1)[0]
                    end_time = time.time()

                    #mem_usage_diff = mem_usage_after - mem_usage_before
                    time_diff = end_time - start_time

                    # Print the map with the optimal path highlighted.
                    self.view.printMap(mapSize=self.settings['mapSize'], worker=self.settings["worker"],
                                       shelves=self.settings["shelves"], path=optimal_path, highlight=destination_list,
                                       rotation=self.settings['rotation'])

                    # Print the directions for the optimal path.
                    self.view.printDirection(path=optimal_path, rotation=self.settings['rotation'],
                                             mapSize=self.settings['mapSize'])

                    print("Destination list: ", destination_list)
                    print("Algorithm: ", self.settings['algorithm'])
                    print(f"Memory usage: {max_mem_usage} MiB")
                    print(f"Running time: {time_diff} seconds")

                    if input('Continue? y/n?') == 'n':
                        break

    def getProduct(self):
        while True:
            # This method is called when the user wants to get a product.
            # It prints the map, asks the user for a destination, and finds the optimal path to the destination.
            self.view.printMap(mapSize=self.settings['mapSize'], worker=self.settings["worker"],
                               shelves=self.settings["shelves"], path=None, rotation=self.settings['rotation'])

            while True:
                method1 = input("Choose your input method\n1: input manually \n2: input order list from file \n")
                if method1 not in ['1', '2']:
                    print('wrong input')
                    continue
                elif method1 == '1':
                    order_list = [self.view.inputDestination(settings=self.settings)]
                    break
                elif method1 == '2':
                    order_list = self.view.inputOrders(settings=self.settings)
                    break

            for destination_list in order_list:
                optimal_path = self.model.get_optimal_path(self.settings, destination_list)

                # Print the map with the optimal path highlighted.
                self.view.printMap(mapSize=self.settings['mapSize'], worker=self.settings["worker"],
                                   shelves=self.settings["shelves"], path=optimal_path, highlight=destination_list,
                                   rotation=self.settings['rotation'])

                # Print the directions for the optimal path.
                self.view.printDirection(path=optimal_path, rotation=self.settings['rotation'],
                                         mapSize=self.settings['mapSize'])
                print("Algorithm: ", self.settings['algorithm'])

                # Ask the user if they want to get another product.
                option = input(
                    "Choose one option: \n1) go get next order! \n2) export results to a file \n3) back to main menu\n")
                if option == "1":
                    continue
                elif option == "2":
                    self.view.exportResult(self.settings, optimal_path, destination_list)
                    continue
                else:
                    return

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
                # The user wants to change the shelves.767
                product_loc = self.view.ReadProductFromFile()
                if product_loc is not None:
                    self.settings['shelves'] = list(set(product_loc.values()))
                    self.settings['products'] = product_loc
            elif choice == "6":
                self.settings['countDown'] = self.view.inputcountDown()
            elif choice == "7":
                # Print the current settings.
                self.view.printCurrentSetting(self.settings)
            elif choice == "8":
                orders = self.view.readOrder()
                if orders is not None:
                    self.settings['orders'] = orders
            elif choice == "9":
                # The user wants to go back to the main menu.
                break
            else:
                # Invalid input.
                print("invalid input, please try again")
