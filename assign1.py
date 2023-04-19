import random


class Lot:
    def __init__(self, setup_option, size=8, num_carts=random.randint(3, 8)):
        self.size = size
        self.num_carts = num_carts
        self.grid = []
        self.cartlist = []
        self.worker_pos=()
        for i in range(size):
            row = []
            for j in range(size):
                row.append(" ")
            self.grid.append(row)
        # random setup
        if setup_option == 'r':
            x = random.randint(0, size - 1)
            y = random.randint(0, size - 1)
            self.grid[x][y] = 'W'
            self.worker_pos=(x,y)

            cart_count = 0
            while cart_count < num_carts:
                x = random.randint(0, size - 1)
                y = random.randint(0, size - 1)
                if self.grid[x][y] == " ":
                    self.grid[x][y] = "C"
                    cart_count += 1
                    self.cartlist.append((x, y))
        # manually setup
        elif setup_option == 'm':
            print("Manually set up the chessboard.")

            while True:
                try:
                    worker_input = input(
                        "Enter the coordinates of the worker (row, column) separated by a space: ").split()
                    worker_row = int(worker_input[0])
                    worker_col = int(worker_input[1])
                    if not (0 <= worker_row < size and 0 <= worker_col < size):
                        raise ValueError("Worker coordinates out of range.")
                    break  # break out of the while loop if input is valid
                except (ValueError, IndexError) as e:
                    print(f"Invalid input format. {e} Please enter two integers separated by a space.")

            # place the worker on the chessboard
            self.grid[worker_row][worker_col] = 'W'
            self.worker_pos = (worker_row, worker_col)
            print(self)

            # place the carts on the chessboard
            cart_count = 0
            while cart_count < num_carts:
                try:
                    cart_input = input(
                        f"Enter the coordinates of cart {cart_count + 1} (row, column) separated by a space: ").split()
                    cart_row = int(cart_input[0])
                    cart_col = int(cart_input[1])
                    if not (0 <= cart_row < size and 0 <= cart_col < size):
                        raise ValueError("Cart coordinates out of range.")
                except (ValueError, IndexError) as e:
                    print(f"Invalid input format. {e} Please enter two integers separated by a space.")
                    continue

                # check if the chosen position is empty
                if self.grid[cart_row][cart_col] == " ":
                    self.grid[cart_row][cart_col] = "C"
                    cart_count += 1
                    self.cartlist.append((cart_row, cart_col))
                    print(self)
                else:
                    print("Position already occupied, please choose another position.")


        else:
            print("setup_option wrong format!")

    def __str__(self):
        s = "  "
        for i in range(self.size):
            s += " %2d " % (i)
        s += "\n"
        s += "  " + "+---" * self.size + "+\n"

        for i in range(self.size):
            for j in range(self.size):
                if j == 0:
                    s += "%2d| %c " % (i, self.grid[i][j])
                else:
                    s += "  {} ".format(self.grid[i][j])
            s += "|\n"
        s += "  " + "+---" * self.size + "+\n"
        return s

    def add_navigation(self, directions):
        direction_dict = {"up": "|", "down": "|", "right": "-", "left": "-"}
        i, j = self.worker_pos
        for direction in directions:
            if direction == "down":
                i += 1
            elif direction == "up":
                i -= 1
            elif direction == "right":
                j += 1
            elif direction == "left":
                j -= 1
            if self.grid[i][j] == " ":
                self.grid[i][j] = direction_dict[direction]

    def print_directions(self, directions):
        i, j = self.worker_pos[0],self.worker_pos[1]
        prev_direction = None
        prev_pos = (i, j)
        steps=1
        for direction in directions:
            if direction != prev_direction and prev_direction!=None:
                # a turn occurs
                if steps >0:
                    print("At ({},{}), take {} step(s) {} to ({},{})".format(prev_pos[0], prev_pos[1], steps,prev_direction, i, j))
                prev_direction = direction
                prev_pos = (i, j)
                steps = 1
            elif direction != prev_direction:
                prev_direction=direction
            else:
                #same direction
                steps += 1
            if direction == "down":
                i += 1
            elif direction == "up":
                i -= 1
            elif direction == "right":
                j += 1
            elif direction == "left":
                j -= 1
            # meet a cart in the middle of the direct line
            if self.grid[i][j] == "C":
                print(
                    "At ({},{}), take {} step(s) {} to ({},{})".format(prev_pos[0], prev_pos[1], steps,
                                                                                        prev_direction, i, j))
                print("Pick up the cart!")
                steps=0
                prev_pos = (i, j)
        print("At ({},{}), take {} step(s) {} to ({},{})".format(prev_pos[0], prev_pos[1], steps,
                                                                                  prev_direction, i, j))
        print("route finished!")


class RoutePlanner:
    def __init__(self, lot):
        self.lot = lot
        self.visited_cart = []

    def get_directions(self,lot):
        directions = []
        curr_pos =lot.worker_pos
        while True:
            cart_pos = self.find_closest_cart(curr_pos)
            self.visited_cart.append(cart_pos)
            if cart_pos == None:
                break
            path = self.get_path(curr_pos, cart_pos)
            directions += path
            curr_pos = cart_pos
        path = self.get_path(curr_pos, lot.worker_pos)
        directions += path
        return directions

    def find_closest_cart(self, pos):
        carts = []
        for i in range(self.lot.size):
            for j in range(self.lot.size):
                if self.lot.grid[i][j] == "C" and (i, j) not in self.visited_cart:
                    carts.append((i, j))
        if len(carts) == 0:
            return None
        closest_cart = carts[0]
        closest_distance = self.get_distance(pos, closest_cart)
        for cart in carts:
            distance = self.get_distance(pos, cart)
            if distance < closest_distance:
                closest_cart = cart
                closest_distance = distance
        return closest_cart

    def get_path(self, start, end):
        path = []
        x_diff = end[0] - start[0]
        y_diff = end[1] - start[1]
        if x_diff > 0:
            path += ["down" for i in range(x_diff)]
        elif x_diff < 0:
            path += ["up" for i in range(abs(x_diff))]
        if y_diff > 0:
            path += ["right" for i in range(y_diff)]
        elif y_diff < 0:
            path += ["left" for i in range(abs(y_diff))]
        return path

    def get_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def main():
    global lot
    size = 0
    number = 0
    while True:
        print("Welcome!")
        print("1) go get carts!")
        print("2) settings")
        print("3) exit")
        choice = input("please choose(1/2/3): ")
        if choice == "1":
            setup_option = input("Would you like manual setup or random setup?(m/r)")
            # assigned size and cart number
            if size != 0 and number != 0:
                lot = Lot(setup_option, size, number)
            # only assigned size
            elif size != 0:
                lot = Lot(size=size, setup_option=setup_option)
            # only assigned cart number
            elif number != 0:
                lot = Lot(num_carts=number, setup_option=setup_option)
            # no preferred setting
            else:
                lot = Lot(setup_option=setup_option)
            print(lot)
            planner = RoutePlanner(lot)
            directions = planner.get_directions(lot)
            lot.add_navigation(directions)
            print(lot)
            lot.print_directions(directions)
        if choice == "2":
            while True:
                print("1)size")
                print("2)number of carts")
                print("3)back to the main menu")
                choice_2 = input("please choose(1/2/3): ")
                if choice_2 == "1":
                    size = int(input("please choose a size(5~25):"))
                elif choice_2 == "2":
                    number = int(input("please choose a number(3~20):"))
                elif choice_2 == "3":
                    break
        if choice == "3":
            break


main()
