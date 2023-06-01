import heapq
from itertools import permutations
import multiprocessing
import copy


class FinderModel:
    def CreateObstacles(self, mapSize, shelves):
        obstacles = [[0 for _ in range(mapSize[1])] for _ in range(mapSize[0])]
        for shelf in shelves:
            obstacles[shelf[0]][shelf[1]] = 1
        return obstacles

    def findPath(self, origin: (int, int), destination: (int, int), obstacles: [[int]]):
        # Define the dimensions of the grid (assuming obstacles is a square 2D array)
        rows, cols = len(obstacles), len(obstacles[0])

        # Create a 2D array to keep track of visited cells
        visited = [[False for _ in range(cols)] for _ in range(rows)]

        # Define a Queue to perform BFS
        queue = [(origin[0], origin[1], [])]

        # Define a function to check if a cell is a valid move
        def isValidMove(row, col):
            # Check if the cell is within the bounds of the grid
            if row < 0 or row >= rows or col < 0 or col >= cols:
                return False
            # Check if the cell is an obstacle
            if obstacles[row][col]:
                return False
            # Check if the cell has already been visited
            if visited[row][col]:
                return False
            return True

        # Run BFS until the destination is found
        while queue:
            row, col, path = queue.pop(0)

            # Check if the current cell is the destination
            if (row, col) == destination:
                return path + [(row, col)]

            # Define the possible moves from the current cell
            moves = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
            for move in moves:
                if isValidMove(move[0], move[1]):
                    queue.append((move[0], move[1], path + [(row, col)]))
                    visited[move[0]][move[1]] = True

        # If the destination was not found, return an empty path
        return []

    def __getPath(self, origin: (int, int), destination: (int, int),
                  obstacles: [[int]]) -> (int, int):

        rows, cols = len(obstacles), len(obstacles[0])
        closest = None
        dist = float('inf')

        potential_destinations = []
        if destination[0] > 0:
            destination_up = (destination[0] - 1, destination[1])
            if obstacles[destination_up[0]][destination_up[1]] != 1:
                potential_destinations.append(destination_up)

        if destination[0] < rows - 1:
            destination_down = (destination[0] + 1, destination[1])
            if obstacles[destination_down[0]][destination_down[1]] != 1:
                potential_destinations.append(destination_down)

        if destination[1] > 0:
            destination_left = (destination[0], destination[1] - 1)
            if obstacles[destination_left[0]][destination_left[1]] != 1:
                potential_destinations.append(destination_left)

        if destination[1] < cols - 1:
            destination_right = (destination[0], destination[1] + 1)
            if obstacles[destination_right[0]][destination_right[1]] != 1:
                potential_destinations.append(destination_right)

        for destination in potential_destinations:
            path = self.findPath(origin, destination, obstacles)
            if path:
                distance = len(path)
                if distance < dist:
                    closest = path
                    dist = distance
        return closest

    def tspDp(self, products: list, obstacles: [[int]]):
        n = len(products)
        dist = [[0] * n for i in range(n)]
        pathCache = [[] for i in range(n)]
        for i in range(n):
            for j in range(n):
                pathCache[i].append([])

        for i in range(n):
            for j in range(i + 1, n):
                pathCache[i][j] = self.findPath(products[i], products[j], obstacles)
                pathCache[j][i] = pathCache[i][j][::-1]
                d = len(pathCache[j][i])
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

        ans, best_path = dp(0, 1)
        path = []
        for i in range(len(best_path) - 1):
            if i != 0:
                path += pathCache[best_path[i]][best_path[i + 1]][1:]
            else:
                path += pathCache[best_path[i]][best_path[i + 1]]

        return ans, path

    def generate_valid_access_points(self, obstacle_matrix, midway_points, number='one'):
        access_points = []
        directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]
        for point in midway_points:
            for direction in directions:
                new_point = (point[0] + direction[0], point[1] + direction[1])
                if 0 <= new_point[0] < len(obstacle_matrix) and 0 <= new_point[1] < len(obstacle_matrix[0]) and \
                        obstacle_matrix[new_point[0]][new_point[1]] == 0:
                    access_points.append(new_point)
                    if number == 'one':
                        break
        return access_points

    def shortest_path(self, maze, obstacles, start, end):
        def is_valid(x, y):
            return 0 <= x < maze[0] and 0 <= y < maze[1] and (x, y) not in obstacles

        def heuristic(x, y):
            return abs(x - end[0]) + abs(y - end[1])

        visited = set()
        queue = [(heuristic(*start), 0, start, [])]
        moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        while queue:
            _, cost, current, path = heapq.heappop(queue)
            if current == end:
                return cost, path + [current]

            if current not in visited:
                visited.add(current)
                for dx, dy in moves:
                    x, y = current[0] + dx, current[1] + dy
                    if is_valid(x, y) and (x, y) not in visited:
                        heapq.heappush(queue, (cost + 1 + heuristic(x, y), cost + 1, (x, y), path + [current]))
        return float('inf'), []

    def generate_adj_matrix(self, maze, obstacles, points):
        adj_matrix = {}
        for i, point1 in enumerate(points):
            adj_matrix[i] = {}
            for j, point2 in enumerate(points):
                if point1 != point2:
                    adj_matrix[i][j], path_coords = self.shortest_path(maze, obstacles, point1, point2)
                    adj_matrix[i][(j, "path")] = path_coords
        return adj_matrix

    def branch_and_bound(self, maze_size, obstacles, obstacle_matrix, start_point, midway_points):

        points = list(set([start_point] + midway_points))
        adj_matrix = self.generate_adj_matrix(maze_size, obstacles, points)

        shortest_path_length = float('inf')
        shortest_path_coords = None

        for path in permutations(range(1, len(points))):
            path = [0] + list(path) + [0]
            path_length = sum(adj_matrix[path[i]][path[i + 1]] for i in range(len(path) - 1))

            if path_length < shortest_path_length:
                shortest_path_length = path_length
                shortest_path_coords = []
                for i in range(len(path) - 1):
                    shortest_path_coords += adj_matrix[path[i]][(path[i + 1], "path")]
                    if i != len(path) - 2:
                        shortest_path_coords.pop()

        return shortest_path_coords

    def BB_multi(self, mapsize, obstacles, start_point, destination_list):
        """
        :param mapsize:
        :param obstacles: list of obstacles' coordinates
        :param start_point:
        :param destination_list: list of destination coordinates, exclude start and end point
        :return: list of nodes' coordinates in optimal path
        """

        def generate_adj_matrix(mapsize, obstacles, start_point, destination_list):
            """
            :param mapsize:
            :param obstacles: list of obstacles' coordinates
            :param start_point:
            :param destination_list: list of destination coordinates, exclude start and end point
            :return: adjacency matrix
            """
            obstacle_matrix = self.CreateObstacles(mapsize, obstacles)
            index_point_list = []
            directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]
            for point in destination_list:
                for direction in directions:
                    new_point = (point[0] + direction[0], point[1] + direction[1])
                    if 0 <= new_point[0] < mapsize[0] and 0 <= new_point[1] < mapsize[1] and \
                            obstacle_matrix[new_point[0]][new_point[1]] == 0:
                        # index_point_list.append(shelve_point; direction; access_point)
                        index_point_list.append(
                            '{},{};{},{};{},{}'.format(point[0], point[1], direction[0], direction[1], new_point[0],
                                                       new_point[1]))
            # print(index_point_list)
            index_point_list.append(
                '{},{};0,0;{},{}'.format(start_point[0], start_point[1], start_point[0], start_point[1]))

            """
            adj_matrix = {
                '1,1;0,-1;1,0': {
                    '1,1;0,-1;1,0': (path_length, [path]),
                    '1,1;-1,0;0,1': (path_length, [path]),
                    ...
            """
            adj_matrix = {}
            for p1 in index_point_list:
                adj_matrix[p1] = {}
                for p2 in index_point_list:
                    if p1.split(';')[0] == p2.split(';')[0]:
                        # if they are in the same shelf location, then the path length is infinite and path is empty
                        adj_matrix[p1][p2] = [float('inf'), []]
                    else:
                        # if they are in different shelf location, then the path length is 1 and path is the two points
                        adj_matrix[p1][p2] = list(self.shortest_path(mapsize, obstacles,
                                                                     tuple(map(int, (p1.split(';')[2].split(',')))),
                                                                     tuple(map(int, (p2.split(';')[2].split(','))))))
            return adj_matrix

        def set_infinity(adj_matrix_ref, rows=None, cols=None):
            """
            :param cols: list of columns to set to infinity, format: ['1,1;0,-1;1,0', '1,1;-1,0;0,1', ...]
            :param rows: list of rows to set to infinity, format: ['1,1;0,-1;1,0', '1,1;-1,0;0,1', ...]
            :param adj_matrix_ref : original adjacency matrix
            :return: adj_matrix after setting rows and cols to infinity
            """
            adj_matrix = copy.deepcopy(adj_matrix_ref)
            if cols is None:
                cols = []
            if rows is None:
                rows = []
            for row in rows:
                for col in adj_matrix[row]:
                    adj_matrix[row][col] = [float('inf'), []]

            for row in adj_matrix:
                for col in cols:
                    adj_matrix[row][col] = [float('inf'), []]
            return adj_matrix

        def calculate_reduced_cost(adj_matrix_ref):
            """
            :param adj_matrix_ref:
            :return: reduced cost matrix
            """
            adj_matrix = copy.deepcopy(adj_matrix_ref)
            reduced_cost = 0
            for row in adj_matrix:
                min_cost = min([adj_matrix[row][col][0] for col in adj_matrix])
                if min_cost == float('inf'):
                    continue
                for col in adj_matrix[row]:
                    adj_matrix[row][col][0] -= min_cost
                reduced_cost += min_cost
            for col in adj_matrix:
                min_cost = min([adj_matrix[row][col][0] for row in adj_matrix])
                if min_cost == float('inf'):
                    continue
                for row in adj_matrix:
                    adj_matrix[row][col][0] -= min_cost
                reduced_cost += min_cost
            return reduced_cost

        def other_access_points(index_list, index):
            """
            :param index_list: list of index points
            :param index: index point
            :return: other access point in the same shelf
            """
            res = []
            for i in index_list:
                if i.split(';')[0] == index.split(';')[0] and i.split(';')[2] != index.split(';')[2]:
                    res.append(i)
            return res

        """ BB_multi function starts here"""

        adj_matrix = generate_adj_matrix(mapsize, obstacles, start_point, destination_list)
        current_row = '{},{};0,0;{},{}'.format(start_point[0], start_point[1], start_point[0], start_point[1])
        optimal_path = []
        while True:

            best_col_index = None
            min_cost = float('inf')
            for col in adj_matrix[current_row]:
                if col.split(';')[2] == col.split(';')[0]:
                    continue
                cost = adj_matrix[current_row][col][0] + calculate_reduced_cost(
                    set_infinity(adj_matrix, rows=[current_row] + other_access_points(list(adj_matrix.keys()), col),
                                 cols=[col] + other_access_points(list(adj_matrix.keys()), col)))
                if cost < min_cost:
                    min_cost = cost
                    best_col_index = col

            if min_cost == float('inf'):
                best_col_index = '{},{};0,0;{},{}'.format(start_point[0], start_point[1], start_point[0],
                                                          start_point[1])

            if optimal_path == []:
                optimal_path += adj_matrix[current_row][best_col_index][1]
            else:
                optimal_path += adj_matrix[current_row][best_col_index][1][1:]
            if best_col_index.split(';')[2] == best_col_index.split(';')[0]:
                break
            adj_matrix = set_infinity(adj_matrix,
                                      rows=[current_row] + other_access_points(list(adj_matrix.keys()), best_col_index),
                                      cols=[best_col_index] + other_access_points(list(adj_matrix.keys()),
                                                                                  best_col_index))
            current_row = best_col_index
        return optimal_path

    def get_optimal_path_process(self, queue, settings, destination_list):
        obstacle_matrix = self.CreateObstacles(
            mapSize=settings['mapSize'],
            shelves=settings['shelves'])
        access_points = self.generate_valid_access_points(obstacle_matrix, destination_list, number='one')

        path = []
        if settings['algorithm'] == 'tspDp':
            _, path = self.tspDp([settings['worker']] + access_points, obstacle_matrix)
        elif settings['algorithm'] == 'branchAndBound':
            path = self.BB_multi(settings['mapSize'], settings['shelves'], settings['worker'], destination_list)

        queue.put(path)

    def get_default_path(self, settings, destination_list):
        obstacle_matrix = self.CreateObstacles(
            mapSize=settings['mapSize'],
            shelves=settings['shelves'])
        access_points = self.generate_valid_access_points(obstacle_matrix, destination_list, number='one')
        points = [settings['worker']] + list(set(access_points)) + [settings['worker']]
        path_coords = []
        for i in range(len(points) - 1):
            path_coords += self.shortest_path(settings['mapSize'], settings['shelves'], points[i], points[i + 1])[1]
        return path_coords

    def get_optimal_path(self, settings, destination_list):
        queue = multiprocessing.Queue()
        process = multiprocessing.Process(target=self.get_optimal_path_process,
                                          args=(queue, settings, destination_list))
        process.start()
        process.join(settings['countDown'])  # Wait for settings['countDown'] seconds

        if process.is_alive():
            print("Terminating process as it took longer than 15 seconds, returning the default path")
            process.terminate()
            process.join()
            path = self.get_default_path(settings, destination_list)
        else:
            path = queue.get()

        return path

def main():
    # Define the origin and destinations
    settings = []
    origin = (0, 0)
    destination = (3, 3)
    testPath = [(0, 0), (0, 3), (4, 3), (3, 1)]
    finderModel = FinderModel()

    # Define the obstacles
    maze_size = (40, 21)
    temp_obstacles = [(18, 0), (16, 0), (14, 0), (18, 4), (16, 4), (24, 20), (14, 4), (22, 20), (21, 4), (19, 4), (17, 4),
                 (11, 8), (18, 8), (16, 8), (14, 8), (19, 8), (15, 8), (18, 12), (16, 12), (21, 12), (12, 0), (15, 12),
                 (10, 0), (18, 16), (8, 0), (20, 16), (11, 16), (16, 16), (12, 4), (10, 4), (37, 18), (8, 4), (7, 8),
                 (12, 8), (10, 8), (9, 12), (7, 12), (14, 12), (12, 12), (10, 12), (9, 16), (7, 16), (14, 16), (4, 0),
                 (12, 16), (2, 0), (10, 16), (20, 2), (1, 4), (6, 4), (4, 4), (20, 6), (8, 8), (6, 8), (20, 10),
                 (8, 12), (6, 12), (8, 16), (6, 16), (30, 0), (18, 2), (26, 18), (16, 2), (24, 18), (14, 2), (22, 18),
                 (2, 4), (27, 18), (11, 6), (18, 6), (16, 6), (14, 6), (21, 6), (19, 6), (17, 6), (11, 10), (15, 6),
                 (18, 10), (16, 10), (21, 10), (19, 10), (17, 10), (15, 10), (20, 14), (11, 14), (18, 14), (16, 14),
                 (2, 16), (28, 0), (26, 0), (24, 0), (18, 18), (21, 18), (32, 0), (17, 18), (12, 6), (10, 6), (9, 10),
                 (13, 6), (7, 10), (14, 10), (12, 10), (10, 10), (7, 14), (14, 14), (12, 14), (10, 14), (22, 0),
                 (20, 0), (14, 18), (12, 18), (10, 18), (19, 18), (20, 4), (8, 6), (6, 6), (20, 8), (8, 10), (6, 10),
                 (20, 12), (8, 14), (6, 14)]
    obstacles = [[0 for j in range(maze_size[1])] for i in range(maze_size[0])]
    for obstacle in temp_obstacles:
        x, y = obstacle
        obstacles[x][y] = 1

    midway_points = [(0, 0), (2, 3), (14, 5), (19, 9)]
    # Find the closest path to any destination
    distance, path = finderModel.tspDp(midway_points, obstacles)

    # Print the result
    if path:
        print("TSP Path found:", path)
    else:
        print("No path found")

    # Example usage

    obstacles = [(18, 0), (16, 0), (14, 0), (18, 4), (16, 4), (24, 20), (14, 4), (22, 20), (21, 4), (19, 4), (17, 4),
                 (11, 8), (18, 8), (16, 8), (14, 8), (19, 8), (15, 8), (18, 12), (16, 12), (21, 12), (12, 0), (15, 12),
                 (10, 0), (18, 16), (8, 0), (20, 16), (11, 16), (16, 16), (12, 4), (10, 4), (37, 18), (8, 4), (7, 8),
                 (12, 8), (10, 8), (9, 12), (7, 12), (14, 12), (12, 12), (10, 12), (9, 16), (7, 16), (14, 16), (4, 0),
                 (12, 16), (2, 0), (10, 16), (20, 2), (1, 4), (6, 4), (4, 4), (20, 6), (8, 8), (6, 8), (20, 10),
                 (8, 12), (6, 12), (8, 16), (6, 16), (30, 0), (18, 2), (26, 18), (16, 2), (24, 18), (14, 2), (22, 18),
                 (2, 4), (27, 18), (11, 6), (18, 6), (16, 6), (14, 6), (21, 6), (19, 6), (17, 6), (11, 10), (15, 6),
                 (18, 10), (16, 10), (21, 10), (19, 10), (17, 10), (15, 10), (20, 14), (11, 14), (18, 14), (16, 14),
                 (2, 16), (28, 0), (26, 0), (24, 0), (18, 18), (21, 18), (32, 0), (17, 18), (12, 6), (10, 6), (9, 10),
                 (13, 6), (7, 10), (14, 10), (12, 10), (10, 10), (7, 14), (14, 14), (12, 14), (10, 14), (22, 0),
                 (20, 0), (14, 18), (12, 18), (10, 18), (19, 18), (20, 4), (8, 6), (6, 6), (20, 8), (8, 10), (6, 10),
                 (20, 12), (8, 14), (6, 14)]
    midway_points = [(2, 3), (14, 5), (19, 9)]

    shortest_path_length, shortest_path_coords = finderModel.branch_and_bound(maze_size, obstacles, origin,
                                                                              midway_points)

    # Print the result
    if path:
        print("Branch & Bound Path found:", shortest_path_coords)
    else:
        print("No path found")


# Call the main function
if __name__ == '__main__':
    main()
