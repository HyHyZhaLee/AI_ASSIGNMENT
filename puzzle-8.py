import matplotlib.pyplot as plt
import numpy as np
import random
from collections import deque
import heapq


# The goal state configuration
goal_state_1 = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
])

goal_state_2 = np.array([
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8]
])

# Define the state class
class State:
    _seq = 0
    
    def __init__(self, state, parent=None, move=None, depth=0):
        self.state = np.array(state)
        self.parent = parent
        self.move = move
        self.depth = depth
        self.seq = State._seq
        State._seq += 1

    def get_possible_moves(self):
        moves = []
        zero_pos = tuple(zip(*np.where(self.state == 0)))[0]
        if zero_pos[0] > 0:  # Up
            new_state = np.copy(self.state)
            new_state[zero_pos], new_state[zero_pos[0]-1, zero_pos[1]] = new_state[zero_pos[0]-1, zero_pos[1]], new_state[zero_pos]
            moves.append(State(new_state, self, 'Up', self.depth + 1))
        if zero_pos[0] < 2:  # Down
            new_state = np.copy(self.state)
            new_state[zero_pos], new_state[zero_pos[0]+1, zero_pos[1]] = new_state[zero_pos[0]+1, zero_pos[1]], new_state[zero_pos]
            moves.append(State(new_state, self, 'Down', self.depth + 1))
        if zero_pos[1] > 0:  # Left
            new_state = np.copy(self.state)
            new_state[zero_pos], new_state[zero_pos[0], zero_pos[1]-1] = new_state[zero_pos[0], zero_pos[1]-1], new_state[zero_pos]
            moves.append(State(new_state, self, 'Left', self.depth + 1))
        if zero_pos[1] < 2:  # Right
            new_state = np.copy(self.state)
            new_state[zero_pos], new_state[zero_pos[0], zero_pos[1]+1] = new_state[zero_pos[0], zero_pos[1]+1], new_state[zero_pos]
            moves.append(State(new_state, self, 'Right', self.depth + 1))
        return moves

    def is_goal(self):
        return np.array_equal(self.state, goal_state_1) or np.array_equal(self.state, goal_state_2)

    def __eq__(self, other):
        return np.array_equal(self.state, other.state)

    def __hash__(self):
        return hash(str(self.state))
    
    def total_cost(self):
        return self.depth + manhattan_distance(self.state)



# BFS algorithm to find the solution
def bfs(initial_state):
    visited = set()
    queue = deque([State(initial_state)])

    while queue:
        current_state = queue.popleft()
        if current_state.is_goal():
            return current_state
        visited.add(current_state)
        for move in current_state.get_possible_moves():
            if move not in visited:
                queue.append(move)
    return None

# Calculate Manhattan distance
def manhattan_distance(state):
    distance = 0
    for value in range(1, 9):  # 1 to 8 tiles
        current_position = np.where(state == value)
        
        if current_position[0].size == 0:
            continue
        
        goal_position_1 = np.where(goal_state_1 == value)
        goal_position_2 = np.where(goal_state_2 == value)
        
        # Compute distance to both goal state and take minimum
        distance_1 = abs(current_position[0][0] - goal_position_1[0][0]) + abs(current_position[1][0] - goal_position_1[1][0])
        distance_2 = abs(current_position[0][0] - goal_position_2[0][0]) + abs(current_position[1][0] - goal_position_2[1][0])
        
        # Update minimum
        distance += min(distance_1, distance_2)
    return distance

# A* algorithm to find the solution
def a_star(initial_state):
    visited = set()
    start_state = State(initial_state)
    frontier = [(start_state.depth + manhattan_distance(initial_state), start_state.depth, start_state.seq, start_state)]

    while frontier:
        _, _, _, current_state = heapq.heappop(frontier)
        if current_state.is_goal():
            return current_state
        visited.add(current_state)
        
        for move in current_state.get_possible_moves():
            if move not in visited:
                new_cost = move.depth + manhattan_distance(move.state)
                heapq.heappush(frontier, (new_cost, move.depth, move.seq, move))
    return None

# Reconstruct the path from the goal state to the initial state
def reconstruct_path(end_state):
    actions = []
    while end_state.parent is not None:
        actions.append(end_state.move)
        end_state = end_state.parent
    return actions[::-1]

def count_inversions(state):
    flattened_state = state.flatten()
    inversions = 0
    for i in range(len(flattened_state)):
        for j in range(i + 1, len(flattened_state)):
            if flattened_state[i] > flattened_state[j] and flattened_state[j] != 0:
                inversions += 1
    return inversions

def find_blank_row_from_bottom(state):
    # Find the row of the blank tile (0), counting from the bottom
    blank_row = np.where(state == 0)[0][0]
    return len(state) - blank_row

def is_solvable(state):
    inversions = count_inversions(state)
    blank_row = find_blank_row_from_bottom(state)
    if blank_row % 2 == 0:  # Even row (counting from the bottom)
        return inversions % 2 != 0  # Solvable if odd number of inversions
    else:  # Odd row
        return inversions % 2 == 0  # Solvable if even number of inversions

# Example usage in generate_random_state
def generate_random_state():
    while True:
        state = np.arange(9)
        np.random.shuffle(state)
        state = state.reshape((3, 3))
        if is_solvable(state):
            return state


# The main function where you type the input to get the output
def main():
    initial_state = []
    print("Enter your puzzle state row by row. Use '0' to represent the blank.")
    for i in range(3):
        row = input(f"Enter row {i+1} with numbers separated by space: ").strip().split()
        initial_state.append([int(n) for n in row])

    # Ask the user to choose the algorithm
    algorithm = input("Type 'bfs' to use Breadth-First Search or 'a*' to use A* Search: ").strip()

    solution_state = None
    if algorithm.lower() == 'bfs':
        solution_state = bfs(initial_state)
    elif algorithm.lower() == 'a*':
        solution_state = a_star(initial_state) 

    if solution_state:
        actions = reconstruct_path(solution_state)
        print("Sequence of actions to solve the puzzle:", actions)
        print("Total cost (number of moves):", len(actions))
    else:
        print("No solution found!")
        
    bfs_costs = []
    a_star_costs = []
    
    for _ in range(1000):
        initial_state = generate_random_state()
        bfs_solution = bfs(initial_state)
        a_star_solution = a_star(initial_state)
        if bfs_solution:
            bfs_costs.append(len(reconstruct_path(bfs_solution)))
        if a_star_solution:
            a_star_costs.append(len(reconstruct_path(a_star_solution)))
            
    avg_bfs_cost = sum(bfs_costs) / len(bfs_costs)
    avg_a_star_cost = sum(a_star_costs) / len(a_star_costs)

    plt.bar(['BFS', 'A*'], [avg_bfs_cost, avg_a_star_cost])
    plt.xlabel('Algorithm')
    plt.ylabel('Average Cost')
    plt.title('Average Path Cost for BFS and A* Algorithms')
    plt.show()
    
if __name__ == "__main__":
    main()
