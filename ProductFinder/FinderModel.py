from tqdm import tqdm


class FinderModel:
    def CreateObstacles(self, mapSize, shelves):
        obstacles = [[0 for _ in range(mapSize[1])] for _ in range(mapSize[0])]
        for shelf in shelves:
            obstacles[shelf[0]][shelf[1]] = 1
        return obstacles

    def findPath(self, origin: (int, int), shelf: (int, int), obstacles: [[int]]):
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
            visited[row][col] = True

            # Check if the current cell is the destination
            if (row, col) == shelf:
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
                obstacles: [[int]]) -> list:
        '''This function takes three arguments:
            origin: The starting point of the path.
            destination: The ending point of the path.
            obstacles: A 2D array of integers, where 1 represents an obstacle and 0 represents an empty space.
        The function returns a list of coordinates that represents the shortest path from the origin to the destination.'''
        # Get the dimensions of the map.
        rows, cols = len(obstacles), len(obstacles[0])

        # Initialize the closest destination and the distance to infinity.
        closest = None
        dist = float('inf')

        # Get all of the potential destinations.
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

        # For each potential destination, find the path to it and store the path if it is shorter than the current shortest path.
        for destination in potential_destinations:
            path = self.findPath(origin, destination, obstacles)
            if path:
                distance = len(path)
                if distance < dist:
                    closest = path
                    dist = distance

        # Return the closest destination.
        return closest

    def tsp(self, products: list, obstacles: [[int]]):
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
    distance, path = finderModel.tsp(testPath, obstacles)

    # Print the result
    if path:
        print("Path found:", path)
    else:
        print("No path found")


# Call the main function
if __name__ == '__main__':
    main()
