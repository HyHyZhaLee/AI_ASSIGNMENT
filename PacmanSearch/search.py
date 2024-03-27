import util
import math
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

    def get_cost_of_actions(self, actions):
        # If every action has a cost of 1, then the total cost is just the number of actions
        return len(actions)

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
    def EuclidDistanceHeuristic(self, state, problem):
        pacman_position, food_collected, corners_visited = state  # Adjusted to unpack all three elements
        food_positions = problem.food_positions  # Assuming you want to compare to all food positions

        # Exclude food that's already been collected if that's what you intend
        remaining_food_positions = [food for food in food_positions if food not in food_collected]

        if not remaining_food_positions:
            return 0

        # Calculate the Euclidean distance to each remaining food dot
        distances = [
            math.sqrt((pacman_position[0] - food[0]) ** 2 + (pacman_position[1] - food[1]) ** 2)
            for food in remaining_food_positions
        ]

        # Return the minimum distance to the closest food dot
        return min(distances)

    def simplify_actions(self, actions):
        simplified_actions = []
        i = 0
        while i < len(actions):
            if i + 1 < len(actions):
                current_action = actions[i]
                next_action = actions[i + 1]
                # Check for opposite actions
                if (current_action == 'East' and next_action == 'West') or (
                        current_action == 'West' and next_action == 'East') or (
                        current_action == 'North' and next_action == 'South') or (
                        current_action == 'South' and next_action == 'North'):
                    i += 2  # Skip the next action
                    continue
            simplified_actions.append(actions[i])
            i += 1
        return simplified_actions

    def bfs_search(self, problem):
        frontier = util.Queue()
        explored = set()

        # Add the initial state to the frontier
        initial_state = problem.get_start_state()

        frontier.push((initial_state, []))

        while not frontier.isEmpty():
            current_state, actions = frontier.pop()

            if problem.is_goal_state(current_state):
                return self.simplify_actions(actions)

            if current_state not in explored:
                explored.add(current_state)

                for action in problem.get_actions(current_state):
                    successor = problem.get_successor(current_state, action)
                    new_actions = actions + [action]
                    frontier.push((successor, new_actions))

        return []

    def a_star_search(self, problem, heuristic=None):
        if heuristic is None:
            heuristic = self.EuclidDistanceHeuristic
        frontier = util.PriorityQueue()
        explored = set()

        # Add the initial state to the frontier with a priority of zero
        initial_state = problem.get_start_state()
        # Pass both the state and the problem to the heuristic function
        frontier.push((initial_state, []), heuristic(initial_state, problem))

        while not frontier.isEmpty():
            current_state, actions = frontier.pop()

            if problem.is_goal_state(current_state):
                return self.simplify_actions(actions)

            if current_state not in explored:
                explored.add(current_state)

                for action in problem.get_actions(current_state):
                    successor = problem.get_successor(current_state, action)
                    new_actions = actions + [action]
                    # Unlike BFS, in A* the priority is the current cost plus the heuristic estimate
                    # Again, pass both the successor state and the problem to the heuristic function
                    priority = problem.get_cost_of_actions(new_actions) + heuristic(successor, problem)
                    frontier.push((successor, new_actions), priority)

        return []

    def ucs_search(self, problem):
        frontier = util.PriorityQueue()
        explored = set()

        # Start with the initial state. The priority is the cost so far, which is 0 for the start state.
        initial_state = problem.get_start_state()
        frontier.push((initial_state, [], 0), 0)  # (state, actions, cost), priority

        while not frontier.isEmpty():
            current_state, actions, current_cost = frontier.pop()

            # Check if we have already explored this state
            if current_state in explored:
                continue

            # Check if current state is the goal state
            if problem.is_goal_state(current_state):
                return self.simplify_actions(actions)

            explored.add(current_state)

            for action in problem.get_actions(current_state):
                successor, cost = problem.get_successor(current_state, action), problem.get_cost_of_actions(
                    actions + [action])
                if successor not in explored:
                    # Add successor to the frontier with the updated cost
                    new_actions = actions + [action]
                    new_cost = current_cost + cost
                    frontier.update((successor, new_actions, new_cost), new_cost)

        return []



if __name__ == "__main__":
    # Read input
    layout_file = "layouts/smallMaze.lay"
    with open(layout_file, 'r') as file:
        # Initialize the problem
        pacman_problem = PacmanProblem(file.read())

    searchStratergy = SearchStrategies()

    bfs_result = searchStratergy.bfs_search(pacman_problem)
    ucs_result = searchStratergy.ucs_search(pacman_problem)
    a_star_result = searchStratergy.a_star_search(pacman_problem, None)

    print("BFS Result:")
    print("Testing 1 run:", bfs_result)
    print("Total cost:", len(bfs_result))
    print()
    print("UCS Result:")
    print("Testing 1 run:", ucs_result)
    print("Total cost:", len(ucs_result))
    print()
    print("A* Result:")
    print("Testing 1 run:", a_star_result)
    print("Total cost:", len(a_star_result))