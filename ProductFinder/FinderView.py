from tqdm import tqdm


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
                    row += " ✌ "
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
        print("Welcome to ProductFinder(Alpha Release Version) by CoGPT")
        print("1) go get product!")
        print("2) settings")
        print("3) exit")
        choice = input("please choose(1/2/3): ")
        return choice

    def printSettingMenu(self):
        print("1) set rotation")
        print("2) set algorithm option")
        print("3) set MapSize")
        print("4) set worker")
        print("5) set shelves")
        print("6) print current setting")
        print("7) back to main menu")
        choice = input("please choose(1~7): ")
        return choice

    def printCurrentSetting(self, setting):
        print("rotation: ", setting['rotation'])
        print("algorithm option:", setting["algorithm"])
        print("map size:", setting["mapSize"])
        print("worker: ", setting["worker"])
        print("shelves: ", setting["shelves"])

    def inputDestination(self):
        dest_input = input("please input your destination(eg. 1 2): ").split()
        dest_row = int(dest_input[0])
        dest_col = int(dest_input[1])
        return (dest_row, dest_col)

    def inputWorker(self, mapSize: (int, int), rotation: int):
        worker_input = input("please input worker location(eg. 1 2): ").split()
        worker_row = int(worker_input[0])
        worker_col = int(worker_input[1])
        return (worker_row, worker_col)

    def inputMapSize(self):
        map_size_input = input("please input map size(rows, colomns)(eg. 40 21): ").split()
        map_size_row = int(map_size_input[0])
        map_size_col = int(map_size_input[1])
        return (map_size_row, map_size_col)

    def inputAlgorithm(self):
        algorithm = input("please input algorithm: ")
        return algorithm

    def inputRotation(self):
        rotation = input("please input rotation: ")
        return int(rotation)

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
