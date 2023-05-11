from tqdm import tqdm


class FinderView:
    def __init__(self):
        return

    def printMap(self, mapSize: (int, int), shelves: [(int, int)], worker: (int, int), path: [(int, int)],
                 highlight: [(int, int)] = [],
                 rotation=0) -> None:
        """
        Prints a map in ascii to the user terminal.

        Args:
            mapSize (Tuple[int, int]): A tuple of integers representing the height and width of the map.
            shelves (List[Tuple[int, int]]): A list of tuples representing the position of all shelves.
            worker (Tuple[int, int]): A tuple representing the position of the worker.
            rotation (int): An integer representing the rotation of the map.

        Returns:
            None
        """

        s = "  "
        for i in range(mapSize[1]):
            s += " %2d " % (i)
        s += "\n"
        s += "  " + "┌───" * mapSize[1] + "┐"
        print(s)
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
            print("%2d│" % i + row)
        print("  └" + "───┘" * mapSize[1])

    def printDirection(self, path: [(int, int)]) -> None:
        """Prints the directions to the user terminal."""
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
                print(
                    f"From ({first_pos[0]},{first_pos[1]}), go {steps} steps {prev_direction} to point ({prev_pos[0]},{prev_pos[1]})")
                first_pos = prev_pos
                steps = 1
                prev_pos = curr_pos
                prev_direction = curr_direction
        print(
            f"From ({first_pos[0]},{first_pos[1]}), go {steps} steps {prev_direction} to point ({curr_pos[0]},{curr_pos[1]})")

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

    def inputWorker(self):
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
