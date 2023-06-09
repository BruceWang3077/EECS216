import sys
from datetime import datetime

class FinderView:
    def __init__(self):
        return

    def printMap(self, mapSize: (int, int), shelves: [(int, int)], worker: (int, int), path: [(int, int)],
                 rotation: int,
                 highlight: [(int, int)] = []) -> None:
        """
        Prints a map in ascii to the user terminal.

        Args:
            mapSize (Tuple[int, int]): A tuple of integers representing the height and width of the map.
            shelves (List[Tuple[int, int]]): A list of tuples representing the position of all shelves.
            worker (Tuple[int, int]): A tuple representing the position of the worker.
            rotation (int): An integer representing the counterclockwise degree of rotation of the map. 0,1 means rotation 0, 90

        Returns:
            None
        """

        if rotation % 2 == 1:
            mapSize = (mapSize[1], mapSize[0])

        if shelves is not None:
            shelves = self.rotateList(mapSize, shelves, rotation)
        if path is not None:
            path = self.rotateList(mapSize, path, rotation)
        if highlight is not None:
            highlight = self.rotateList(mapSize, highlight, rotation)
        if worker is not None:
            worker = self.rotateTuple(mapSize, worker, rotation)

        s = "  "
        for i in range(mapSize[1]):
            s += " %2d " % (i)
        s += "\n"
        if rotation == 0:
            print(s)
        top = "  " + "┌───" * mapSize[1] + "┐"
        print(top)
        for i in range(mapSize[0]):
            row = ""
            for j in range(mapSize[1]):
                if (i, j) == worker:
                    # row += " ✌ "
                    row += " ✪ "
                elif (i, j) in shelves:
                    if (i, j) in highlight:
                        row += "▓◎▓"
                    else:
                        row += "▓▓▓"
                elif (i, j) in highlight:
                    row += " ◎ "
                elif path != None and (i, j) in path:
                    row += " * "
                else:
                    row += "   "
                if j == mapSize[1] - 1:
                    row += "│"
                else:
                    row += " "
            if rotation == 0:
                print("%2d│" % i + row)
            elif rotation == 1:
                print("%2d│" % (mapSize[0] - 1 - i) + row)
        print("  └" + "───┘" * mapSize[1])
        if rotation == 1:
            print(s)

    def rotateList(self, mapSize: (int, int), list: [(int, int)], rotation: int):
        new_list = []
        if rotation == 0:
            new_list = list
        elif rotation == 1:
            for tuple in list:
                x = mapSize[0] - 1 - tuple[1]
                y = tuple[0]
                new_list.append((x, y))
        elif rotation == 2:
            for tuple in list:
                x = mapSize[0] - 1 - tuple[0]
                y = mapSize[1] - 1 - tuple[1]
                new_list.append((x, y))
        elif rotation == 3:
            for tuple in list:
                x = tuple[1]
                y = mapSize[1] - 1 - tuple[0]
                new_list.append((x, y))
        return new_list

    def rotateTuple(self, mapSize: (int, int), tuple: (int, int), rotation: int):
        x, y = tuple
        if rotation == 1:
            x = mapSize[0] - 1 - tuple[1]
            y = tuple[0]
        elif rotation == 2:
            x = mapSize[0] - 1 - tuple[0]
            y = mapSize[1] - 1 - tuple[1]
        elif rotation == 3:
            x = tuple[1]
            y = mapSize[1] - 1 - tuple[0]
        tuple = (x, y)
        return tuple

    def reverseTuple(self, mapSize: (int, int), tuple: (int, int), rotation: int):
        x, y = tuple
        if rotation == 1:
            x = tuple[1]
            y = mapSize[0] - 1 - tuple[0]
        elif rotation == 2:
            x = mapSize[0] - 1 - tuple[0]
            y = mapSize[1] - 1 - tuple[1]
        elif rotation == 3:
            x = mapSize[1] - 1 - tuple[1]
            y = tuple[0]
        tuple = (x, y)
        return tuple

    def printDirection(self, path: [(int, int)], rotation: int, mapSize: (int, int)) -> None:
        """Prints the directions to the user terminal."""
        if rotation % 2 == 1:
            mapSize = (mapSize[1], mapSize[0])
        path = self.rotateList(mapSize, path, rotation)
        curr_direction = ""
        prev_direction = ""
        steps = 1
        first_pos = path[0]
        sec_pos = path[1]
        if first_pos[0] == sec_pos[0]:
            prev_direction = "right" if first_pos[1] < sec_pos[1] else "left"
            steps = abs(first_pos[1] - sec_pos[1])
        elif first_pos[1] == sec_pos[1]:
            prev_direction = "down" if first_pos[0] < sec_pos[0] else "up"
            steps = abs(first_pos[0] - sec_pos[0])
        prev_pos = sec_pos
        for i in range(2, len(path)):
            curr_pos = path[i]
            if prev_pos[0] == curr_pos[0]:
                curr_direction = "right" if prev_pos[1] < curr_pos[1] else "left"
            elif prev_pos[1] == curr_pos[1]:
                curr_direction = "down" if prev_pos[0] < curr_pos[0] else "up"
            if curr_direction == prev_direction:
                steps += 1
                prev_pos = curr_pos
            else:
                reverse_first_pos = self.reverseTuple(mapSize=mapSize, rotation=rotation, tuple=first_pos)
                reverse_prev_pos = self.reverseTuple(mapSize=mapSize, rotation=rotation, tuple=prev_pos)
                print(
                    f"From ({reverse_first_pos[0]},{reverse_first_pos[1]}), go {steps} steps {prev_direction} to point ({reverse_prev_pos[0]},{reverse_prev_pos[1]})")
                first_pos = prev_pos
                steps = 1
                prev_pos = curr_pos
                prev_direction = curr_direction
        reverse_first_pos = self.reverseTuple(mapSize=mapSize, rotation=rotation, tuple=first_pos)
        reverse_curr_pos = self.reverseTuple(mapSize=mapSize, rotation=rotation, tuple=curr_pos)
        print(
            f"From ({reverse_first_pos[0]},{reverse_first_pos[1]}), go {steps} steps {prev_direction} to point ({reverse_curr_pos[0]},{reverse_curr_pos[1]})")

    def printMainMenu(self):
        while True:
            try:
                print("Welcome to ProductFinder(Final Release Version) by CoGPT")
                print("1) go get product!")
                print("2) settings")
                print('3) run tests')
                print("4) exit")
                choice = input("please choose(1/2/3/4): ")
                if int(choice) not in range(1, 5):
                    raise ValueError
                return choice
            except ValueError:
                print("Error: Invalid input. Please enter an integer between 1 and 4.")

    def printSettingMenu(self):
        while True:
            try:
                print("1) set rotation")
                print("2) set algorithm option")
                print("3) set MapSize")
                print("4) set worker")
                print("5) set shelves")
                print("6) set countDown")
                print("7) print current setting")
                print("8) input orders via file")
                print("9) back to main menu")
                choice = input("please choose(1~9): ")
                if int(choice) not in range(1, 10):
                    raise ValueError
                return choice
            except ValueError:
                print("Error: Invalid input. Please enter an integer between 1 and 9.")

    def printCurrentSetting(self, setting):
        print("rotation: ", setting['rotation'])
        print("algorithm option:", setting["algorithm"])
        print("map size:", setting["mapSize"])
        print("worker: ", setting["worker"])
        print("shelves: ", setting["shelves"])
        print("countDown: ", setting["countDown"])

    def inputDestination(self, settings):
        method = input("Choose your input method\n1: input by (x,y) \n2: input by product ID \n")
        destination_number = int(input('how many destination do you want to input? '))
        destination_list = []
        i = 0
        while i < destination_number:
            if method == '1':
                destination_input = input("please input your #{} product coordinates(eg. 1 2): ".format(i+1)).split()
                if len(destination_input) != 2:
                    print('wrong input format')
                    continue
                destination_row = int(destination_input[0])
                destination_col = int(destination_input[1])
                if destination_row < 0 or destination_row > settings['mapSize'][0] or destination_col < 0 or destination_col > settings['mapSize'][1]:
                    print('coordinate out of range')
                    continue
            elif method == '2':
                destination_product = input("please input your #{} product ID: ".format(i+1))
                try:
                    destination_row = settings['products'][destination_product][0]
                    destination_col = settings['products'][destination_product][1]
                except:
                    print('product ID not found')
                    continue

            destination_list.append((destination_row, destination_col))
            i+=1
        return destination_list

    def inputOrders(self, settings):
        order_list = []
        while True:
            filename = input("Please input file path:")
            try:
                f = open(filename, "r")
                for line in f.readlines():
                    product_list = []
                    for productID in line.strip().split(', '):
                        try:
                            destination_row = settings['products'][productID][0]
                            destination_col = settings['products'][productID][1]
                            product_list.append((destination_row, destination_col))
                        except:
                            print('product ID {} not found'.format(productID))
                            continue

                    order_list.append(product_list)
                return order_list
            except FileNotFoundError:
                print(f"Error: File '{filename}' not found.")

    def inputWorker(self, mapSize: (int, int), rotation: int):
        try:
            worker_input = input("please input worker location(eg. 1 2): ").split()
            worker_row, worker_col = map(int, worker_input)
            if 0 < worker_row <= mapSize[0] and 0 < worker_col <= mapSize[1]:
                return (worker_row, worker_col)
            else:
                raise ValueError
        except ValueError:
            print(
                "Error: Invalid input. Please enter two integers separated by a space, within the bounds of the map size.")
            return (0, 0)

    def inputMapSize(self):
        try:
            map_size_input = input("please input map size(rows, columns)(eg. 40 21): ").split()
            assert len(map_size_input) == 2
            map_size_row, map_size_col = map(int, map_size_input)
            if map_size_row > 0 and map_size_col > 0:
                return (map_size_row, map_size_col)
            else:
                raise ValueError
        except (ValueError, AssertionError):
            print("Error: invalid input. Please enter two positive integers separated by a space.")
            return (40, 21)

    def inputAlgorithm(self):
        try:
            algorithm = input("1) tspDp \n2) Branch & Bound\n3) Nearest Neighbor\nplease choose an algorithm(1 or 2 or 3):")
            assert algorithm in ['1', '2','3']
            if algorithm == '1':
                return 'tspDp'
            elif algorithm == '2':
                return 'branchAndBound'
            elif algorithm == '3':
                return "NearestNeighbor"
        except AssertionError:
            print("Error: invalid input. Please enter either '1' or '2'.")
            return 'tspDp'

    def inputRotation(self):
        rotation = input("please input rotation: ")
        try:
            rotation = int(rotation)
            if rotation < 1 or rotation > 4:
                raise ValueError
        except ValueError:
            print("Error: rotation should be an integer in the range of 1 to 4.")
            return 1
        else:
            return int(rotation)

    def inputcountDown(self):
        countDown = input("please input countDown number(second): ")
        try:
            countDown = int(countDown)
            if countDown < 1:
                raise ValueError
        except ValueError:
            print("Error: countDown should be a positive integer.")
            return 15
        else:
            return int(countDown)

    '''
    def inputShelves(self):
        file = open(input("please input file path:"), "r")
        count_dict = {}
        next(file)
        for line in tqdm(file):
            ID, X, Y = line.split('\t')
            # drop the decimal part
            X = int(float(X))
            Y = int(float(Y))
            count_dict[(X, Y)] = count_dict.get((X, Y), 0) + 1
        shelves = list(count_dict.keys())
        return shelves, count_dict
    '''

    def ReadProductFromFile(self):
        filename = input("Please input file path:")
        try:
            file = open(filename, "r")
            product_dict = {}
            next(file)
            for line in file:
                ID, X, Y = line.split('\t')
                # drop the decimal part
                X = int(float(X))
                Y = int(float(Y))
                product_dict[ID] = (X, Y)
            # print(product_dict)
            return product_dict
        except FileNotFoundError:
            print(f"Error: file '{filename}' not found.")
            return None

    def exportResult(self, settings, optimal_path, destination_list):
        # Get the current date and time
        now = datetime.now()
        formatted_date_time = now.strftime("%m-%d_%H-%M-%S")

        # Create a file name with the current date and time
        file_name = f'Navigation_{formatted_date_time}.txt'

        # Redirect the standard output to a file
        with open(file_name, 'w', encoding='utf-8') as file:
            sys.stdout = file
            self.printMap(mapSize=settings['mapSize'], worker=settings["worker"],
                               shelves=settings["shelves"], path=optimal_path, highlight=destination_list,
                               rotation=settings['rotation'])

            # Print the directions for the optimal path.
            self.printDirection(path=optimal_path, rotation=settings['rotation'],
                                     mapSize=settings['mapSize'])

        # Reset the standard output to the original stream
        sys.stdout = sys.__stdout__
        print(f'Output file: {file_name}')



