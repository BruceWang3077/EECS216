from tqdm import tqdm
import heapq
from itertools import permutations

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

    def getPath(self, origin: (int, int), destination: (int, int),
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

    def branch_and_bound(self, maze_size, obstacles, obstacle_matrix, start_point, midway_points):
        def generate_valid_access_points(obstacle_matrix, midway_points):
            access_points = []
            directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]
            for point in midway_points:
                for direction in directions:
                    new_point = (point[0] + direction[0], point[1] + direction[1])
                    if 0 <= new_point[0] < maze_size[0] and 0 <= new_point[1] < maze_size[1] and obstacle_matrix[new_point[0]][new_point[1]] == 0:
                        access_points.append(new_point)
                        break
            return access_points
        def generate_adj_matrix(maze, obstacles, points):
            adj_matrix = {}
            for i, point1 in enumerate(points):
                adj_matrix[i] = {}
                for j, point2 in enumerate(points):
                    if point1 != point2:
                        adj_matrix[i][j], path_coords = shortest_path(maze, obstacles, point1, point2)
                        adj_matrix[i][(j, "path")] = path_coords
            return adj_matrix

        def shortest_path(maze, obstacles, start, end):
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

        access_points = generate_valid_access_points(obstacle_matrix, midway_points)
        points = list(set([start_point] + access_points))
        adj_matrix = generate_adj_matrix(maze_size, obstacles, points)

        shortest_path_length = float('inf')
        shortest_path_coords = None

        for path in tqdm(permutations(range(1, len(points)))):
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


def main():
    # Define the origin and destinations
    settings = []
    origin = (0, 0)
    destination = (3, 3)
    testPath = [(0, 0), (0, 3), (4, 3), (3, 1)]
    finderModel = FinderModel()

    # Define the obstacles
    obstacles = [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0]
    ]

    # Find the closest path to any destination
    distance, path = finderModel.tspDp(testPath, obstacles)

    # Print the result
    if path:
        print("TSP Path found:", path)
    else:
        print("No path found")

    # Example usage
    maze_size = (40, 21)
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

    shortest_path_length, shortest_path_coords = branch_and_bound(maze_size, obstacles, origin, midway_points)

    # Print the result
    if path:
        print("Branch & Bound Path found:", shortest_path_coords)
    else:
        print("No path found")


# Call the main function
if __name__ == '__main__':
    main()
