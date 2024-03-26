import util
import random
from game import Directions

class PacmanProblem:
    def __init__(self, layout_str):
        self.layout, self.pacman_position, self.food_positions, self.corners = self.parse_layout_from_string(layout_str)

    def get_start_state(self):
        return (self.pacman_position, tuple(), tuple(self.corners))

    def get_actions(self, state):
        pacman_pos, _, _ = state
        legal_actions = []
        if self.layout[pacman_pos[0]][pacman_pos[1] - 1] != '%':
            legal_actions.append('West')
        if self.layout[pacman_pos[0]][pacman_pos[1] + 1] != '%':
            legal_actions.append('East')
        if self.layout[pacman_pos[0] - 1][pacman_pos[1]] != '%':
            legal_actions.append('North')
        if self.layout[pacman_pos[0] + 1][pacman_pos[1]] != '%':
            legal_actions.append('South')
        return legal_actions

    def get_successor(self, state, action):
        pacman_pos, food_collected, corners_visited = state
        new_pacman_pos = self.calculate_new_position(pacman_pos, action)
        if new_pacman_pos in self.food_positions:
            food_collected += (new_pacman_pos,)
        if new_pacman_pos in self.corners:
            corners_visited += (new_pacman_pos,)
        return (new_pacman_pos, food_collected, corners_visited)

    def is_goal_state(self, state):
        return len(state[1]) == len(self.food_positions) and len(state[2]) == len(self.corners)

    def parse_layout_from_string(self, layout_str):
        layout = []
        pacman_position = None
        food_positions = []
        corners = []

        # Loại bỏ các dòng không cần thiết trước và sau layout
        # và loại bỏ bất kỳ dòng nào chứa "Score:"
        cleaned_lines = [line for line in layout_str.splitlines() if line.strip() and "Score:" not in line]

        for row_idx, line in enumerate(cleaned_lines):
            row = list(line.strip())
            for col_idx, char in enumerate(row):
                if char == 'P' or char == '<' or char == '^' or char == '>' or char == 'v':
                    pacman_position = (row_idx, col_idx)
                elif char == '.':
                    food_positions.append((row_idx, col_idx))
                elif char == '%':
                    # Wall
                    pass
            layout.append(row)

        # Xác định các góc
        layout_height, layout_width = len(layout), len(layout[0])
        corners = [(0, 0), (0, layout_width - 1), (layout_height - 1, 0), (layout_height - 1, layout_width - 1)]

        return layout, pacman_position, food_positions, corners

    def calculate_new_position(self, current_pos, action):
        x, y = current_pos
        if action == 'West':
            return (x, y - 1)
        elif action == 'East':
            return (x, y + 1)
        elif action == 'North':
            return (x - 1, y)
        elif action == 'South':
            return (x + 1, y)
        return current_pos

class SearchStrategies:
    @staticmethod
    def bfs_search(problem):
        frontier = util.Queue()
        explored = set()

        # Add the initial state to the frontier
        initial_state = problem.get_start_state()
        frontier.push((initial_state, []))

        while not frontier.isEmpty():
            current_state, actions = frontier.pop()

            if problem.is_goal_state(current_state):
                return actions

            if current_state not in explored:
                explored.add(current_state)

                for action in problem.get_actions(current_state):
                    successor = problem.get_successor(current_state, action)
                    new_actions = actions + [action]
                    frontier.push((successor, new_actions))

        return []

    @staticmethod
    def a_star_search(problem, heuristic=None):
        frontier = util.PriorityQueue()
        explored = set()

        # Add the initial state to the frontier with priority based on heuristic
        initial_state = problem.get_start_state()
        priority = 0 if heuristic is None else heuristic(initial_state)
        frontier.push((initial_state, []), priority)

        while not frontier.isEmpty():
            current_state, actions = frontier.pop()

            if problem.is_goal_state(current_state):
                return actions

            if current_state not in explored:
                explored.add(current_state)

                for action in problem.get_actions(current_state):
                    successor = problem.get_successor(current_state, action)
                    new_actions = actions + [action]
                    cost = len(new_actions)
                    priority = cost + (0 if heuristic is None else heuristic(successor))
                    frontier.push((successor, new_actions), priority)

        return []


if __name__ == "__main__":
    # Read input
    layout_file = "layouts/smallMaze.lay"
    with open(layout_file, 'r') as file:
        # Initialize the problem
        pacman_problem = PacmanProblem(file.read())

    # Run BFS
    bfs_result = SearchStrategies.bfs_search(pacman_problem)
    print("BFS Result:")
    print("List of actions:", bfs_result)
    print("Total cost:", len(bfs_result))
    print()

    # Run A* with a heuristic function
    heuristic_function = None  # Replace with your heuristic function if needed
    a_star_result = SearchStrategies.a_star_search(pacman_problem, heuristic_function)
    print("A* Result:")
    print("List of actions:", a_star_result)
    print("Total cost:", len(a_star_result))