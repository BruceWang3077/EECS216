import random

class Lot:
    def __init__(self, size=8, num_carts=random.randint(3,8)):
        self.size = size
        self.num_carts = num_carts
        self.grid = []
        for i in range(size):
            row = []
            for j in range(size):
                if i == 0 and j == 0:
                    row.append("S")
                else:
                    row.append(" ")
            self.grid.append(row)

        cart_count=0
        while cart_count<num_carts:
            x=random.randint(0,size-1)
            y=random.randint(0,size-1)
            if self.grid[x][y]==" ":
                self.grid[x][y]="C"
                cart_count+=1



    def __str__(self):
        s = "  "
        for i in range(self.size):
            s+=" %2d "%(i)
        s+="\n"
        s += "  " + "+---" * self.size + "+\n"

        for i in range(self.size):
            for j in range(self.size):
                if j == 0:
                    s+="%2d| %c "%(i,self.grid[i][j])
                else:
                    s += "  {} ".format(self.grid[i][j])
            s += "|\n"
        s += "  "+"+---" * self.size + "+\n"
        return s

    def add_navigation(self, directions):
        direction_dict = {"up": "|", "down": "|", "right": "-", "left": "-"}
        i,j=0,0
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
        i, j = 0, 0
        for direction in directions:
            print("({},{})".format(i, j), end=" -> ")
            if direction == "down":
                i += 1
            elif direction == "up":
                i -= 1
            elif direction == "right":
                j += 1
            elif direction == "left":
                j -= 1
            print("({},{})".format(i, j), end=" ")
            if self.grid[i][j] == "C":
                print("pick up the cart!")
            elif self.grid[i][j] == "S":
                print("route finished!")
            else:
                print('')


class RoutePlanner:
    def __init__(self, lot):
        self.lot = lot
        self.visited_cart = []

    def get_directions(self):
        directions = []
        curr_pos = (0, 0)
        while True:
            cart_pos = self.find_closest_cart(curr_pos)
            self.visited_cart.append(cart_pos)
            if cart_pos == None:
                break
            path = self.get_path(curr_pos, cart_pos)
            directions += path
            curr_pos = cart_pos
        path = self.get_path(curr_pos, (0, 0))
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
            if size != 0 and number != 0:
                lot = Lot(size, number)
            elif size != 0:
                lot = Lot(size=size)
            elif number != 0:
                lot = Lot(num_carts=number)
            else:
                lot = Lot()
            print(lot)
            planner = RoutePlanner(lot)
            directions = planner.get_directions()
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
