import random
import re


def generate_map():
    """Generates a random map of size map_size x map_size with num_carts shopping carts."""
    # generate random shopping cart positions
    if worker_manual is not True:
        position = (random.randint(0, map_size - 1), random.randint(0, map_size - 1))
    else:
        position = worker_position
    if cart_manual is not True:
        carts.clear()
        num_carts = random.randint(min_cart_size, max_cart_size)
        while len(carts) < num_carts:
            x = random.randint(0, map_size - 1)
            y = random.randint(0, map_size - 1)
            if (x, y) not in carts and (x, y) != position:
                carts.append((x, y))
    # generate map
    graph = {}
    for i in range(map_size):
        for j in range(map_size):
            if (i, j) in carts:
                graph[(i, j)] = 'cart'
            else:
                graph[(i, j)] = 'empty'
    return position, graph, carts


def print_map(graph):
    """Prints a visual representation of the map."""
    print('Legend:')
    print('W: Worker')
    print('C: Cart')
    print('.: Empty space')
    print('Coordinates are (row, col)')
    print()
    print('  ', end='')
    for i in range(map_size):
        if i < 10:
            print(f'{i} ', end='')
        else:
            print(f'{i}', end='')
    print()
    for i in range(map_size):
        if i < 10:
            print(f'{i} ', end='')
        else:
            print(f'{i}', end='')
        for j in range(map_size):
            if (i, j) == worker_position:
                print('W', end=' ')
            elif graph[(i, j)] == 'cart':
                print('C', end=' ')
            else:
                print('.', end=' ')
        print()



def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def tsp(carts):
    n = len(carts)
    dist = [[0] * n for i in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            d = manhattan_distance(carts[i], carts[j])
            dist[i][j] = d
            dist[j][i] = d

    memo = {}

    def dp(pos, visited):
        if (pos, visited) in memo:
            return memo[(pos, visited)]

        if visited == (1 << n) - 1:
            return dist[pos][0], [pos, 0]

        ans, best_path = float('inf'), []
        for i in range(n):
            if visited & (1 << i) == 0:
                new_visited = visited | (1 << i)
                sub_ans, sub_path = dp(i, new_visited)
                total_dist = dist[pos][i] + sub_ans
                if total_dist < ans:
                    ans = total_dist
                    best_path = [pos] + sub_path[:]

        memo[(pos, visited)] = ans, best_path
        return ans, best_path

    return dp(0, 1)


def calculate_distance(path):
    distance = 0
    for i in range(len(path) - 1):
        if path[i] is None or path[i + 1] is None:
            continue
        x1, y1 = path[i]
        x2, y2 = path[i + 1]
        distance += abs(x2 - x1) + abs(y2 - y1)
    return distance


def main():
    global map_size, max_cart_size, min_cart_size, cart_manual, carts, worker_position, worker_manual
    print('Welcome to tsp-shopping-cart solver')
    while True:
        print('\n 1) Generate a random graph and find the shortest path \n 2) Customize the graph and number of '
              'shopping carts \n 3) Exit')
        choice = input()
        if choice == '3':
            print("Goodbye!")
            break
        elif choice == '1':
            worker_position, graph, carts = generate_map()
            print("Generated the following graph:")
            print_map(graph)
            carts.insert(0, (0, 0))
            distance, path = tsp(carts)
            print("The shortest path is:")
            for i in range(len(path) - 1):
                current_pos = carts[path[i]]
                next_pos = carts[path[i + 1]]
                print(
                    "Worker begins at ({},{}), moves to ({},{}).".format(current_pos[0], current_pos[1], next_pos[0],
                                                                         next_pos[1]))
            print("Total distance traveled: {}".format(distance))
            print('Problem solved. Back to main menu.')
        elif choice == '2':
            while True:
                print('\n 1) carts  \n 2) worker \n 3) map \n 4) Exit')
                choice = input()
                if choice == '1':
                    while True:
                        print('\n 1) max cart number  \n 2) min cart number \n 3) manual mode \n 4) Exit')
                        choice = input()
                        if choice == '1':
                            max_cart_size = int(input(
                                "Please enter the maximum cart size (default 5, must be an integer greater than or "
                                "equal to 1): "))
                            print("setting succeed")
                        elif choice == '2':
                            min_cart_size = int(input(
                                "Please enter the minimum cart size (default 5, must be an integer greater than or "
                                "equal to 1): "))
                            print("setting succeed")
                        elif choice == '3':
                            # Prompt the user to input a comma-separated list of tuples
                            cart_input = input("Enter the carts in the format of (x1, y1), (x2, y2), ...: ")
                            nums = re.findall(r'\d+', cart_input)
                            carts = [(int(nums[i]), int(nums[i + 1])) for i in range(0, len(nums), 2)]
                            cart_manual = True
                            print("setting succeed")
                        elif choice == '4':
                            # Code to adjust map size
                            break
                elif choice == '2':
                    while True:
                        print('\n 1) manual mode \n 2) random mode \n 3) Exit')
                        choice = input()
                        if choice == '1':
                            worker_position = input(
                                "Enter the worker position in the format of (x, y)")
                            worker_manual = True
                            print("setting succeed")
                        elif choice == '2':
                            worker_manual = False
                            print("setting succeed")
                        elif choice == '3':
                            break
                elif choice == '3':
                    map_size = int(input(
                        "Please enter the maximum cart size (default 5, must be an integer from 5 to 20): "))
                    while map_size < 5 or map_size > 20:
                        map_size = int(
                            input("Invalid maximum cart size. Please enter an integer from 5 to 20: "))
                    print("setting succeed")
                elif choice == '4':
                    break

        else:
            print("Invalid input!")


if __name__ == "__main__":
    max_cart_size = 5
    min_cart_size = 2
    map_size = 5
    cart_manual = False
    worker_manual = False
    carts = []
    worker_position = (0, 0)
    main()
