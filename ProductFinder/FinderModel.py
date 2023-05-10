from tqdm import tqdm

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


def main():
    # Define the origin and destinations
    settings = []
    origin = (0, 0)
    destination = (3, 3)
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
    path = finderModel.getPath(origin, destination, obstacles)

    # Print the result
    if path:
        print("Path found:", path)
    else:
        print("No path found")


# Call the main function
if __name__ == '__main__':
    main()
