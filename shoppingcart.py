import random
import numpy as np


class Lot:
    def __init__(self, setup_option, size=8, num_carts=random.randint(3, 8)):
        self.size = size
        self.num_carts = num_carts
        self.grid = []
        self.cartlist = []
        self.worker_pos=()
        self.adj_matrix=np.zeros((num_carts+1,num_carts+1))
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
        self.get_adj_matrix()

    def get_adj_matrix(self):
        nodes=[self.worker_pos]
        nodes+=self.cartlist
        for i in range(len(nodes)):
            for j in range(i+1, len(nodes)):
                dis=get_distance(nodes[i],nodes[j])
                self.adj_matrix[i][j]=dis
                self.adj_matrix[j][i]=dis


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
        new_directions=[]
        for direction in directions:
            new_directions+=direction

        for direction in new_directions:
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
        for one_directions in directions:
            for direction in one_directions:
                if direction != prev_direction and prev_direction!=None:
                    # a turn occurs
                    if steps >0:
                        print("At ({},{}), take {} step(s) {} to ({},{})".format(prev_pos[0], prev_pos[1], steps,prev_direction, i, j))
                    prev_direction = direction
                    prev_pos = (i, j)
                    steps = 1
                elif prev_direction is None:
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
    def __init__(self, lot,algo_option):
        self.lot = lot
        self.visited_cart = []
        self.algo_option=algo_option

    def get_directions(self,lot):
        curr_pos=lot.worker_pos
        directions=[]
        if self.algo_option=='1':
            carts=lot.cartlist.copy()
        else:
            carts=self.optimal_order(lot)
        while carts:
            cart=carts.pop(0)
            path=self.get_path(curr_pos,cart)
            directions.append(path)
            curr_pos=cart
        path=self.get_path(curr_pos,lot.worker_pos)
        directions.append(path)
        return directions

    def optimal_order(self,lot):
        orders= []
        visited=[False]*(lot.num_carts+1)
        permutation=[]
        node=0
        distance=0
        self.dfs(node,visited, permutation,distance,orders,lot)
        optimal_order = min(orders, key=lambda x: x[1])
        optimal_order=optimal_order[0]
        optimal_order.pop(0)
        cart_list=[]
        for cart in optimal_order:
            cart=lot.cartlist[cart-1]
            cart_list.append(cart)
        return cart_list

    def dfs(self,node,visited,permutation,distance,orders,lot):
        visited[node]=True
        if node!=0:
            prev_node=permutation.pop()
            distance+=lot.adj_matrix[prev_node][node]
            permutation.append(prev_node)
        permutation.append(node)
        if len(permutation)==lot.num_carts+1:
            orders.append((permutation.copy(),distance))
        else:
            for neighbor in range(lot.num_carts+1):
                if not visited[neighbor]:
                    self.dfs(neighbor,visited,permutation,distance,orders,lot)
        permutation.pop()
        visited[node]=False





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

def get_distance(pos1, pos2):
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
            print("1)pick up carts in random order")
            print("2)pick up carts in an optimal order")
            algo_option=input("please choose(1/2):")
            planner = RoutePlanner(lot,algo_option)
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
                    number = int(input("please choose a number(3~10):"))
                elif choice_2 == "3":
                    break
        if choice == "3":
            break


main()
