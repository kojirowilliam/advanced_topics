# [[# of circles on left, # of polys on left], [# of circles on right, # of polys on right], boolean basketSide]
# Initial State: [[3,3], [0,0], False]
# Goal Test: [[0,0], [3,3], True]
# Actions: [#_of_circles_to_move,#_of_polygons_to_move] Each can only either be a 0,1, or 2. [0,0] means move the basket
# Path Cost:

# state = [[3,3], [0,0], False] # [[circles on left, polys on left],[circles on right, polys on right],boolean basketSide]
# goal_state = [[0,0], [3,3], True]
# action = [0,0, True] # [circles_to_transport, polys_to_transport, is_on_left]
# possible_actions = [[0,0], [1,0], [2,0], [0,1], [0,2], [1,1], [1, 2], [2,2]]
# solution = [] # Action History


class Problem():
    def __init__(self,initial, goal_state, possible_actions):
        self.initial = initial
        self.goal_state = goal_state
        self.possible_actions = possible_actions

    def is_goal(self, state):
        '''
        Returns True if the goal isn't reached and False if it reached.

        Parameters
        ----------
        state : list
        [[circles on left, polys on left],[circles on right, polys on right],boolean basketSide]
        The current state of the environment.

        Returns
        -------
        bool
        True if the goal isn't reached and False if the goal is reached.
        '''

        if state == goal_state:
            return True
        else:
            return False


class Node():
    def __init__(self, state, path = []):
        self.state = state
        self.path = path


    def set_state(self, state):
        self.state = state

    def set_path(self, path):
        self.path = path

    def get_state(self):
        return self.state

    def get_path(self):
        return self.path

# def next_action(action):
#     '''
#
#     Parameters
#     ----------
#     action : list
#     [circles_to_transport, polys_to_transport, is_on_left]
#     The action the environment just took make.
#
#     Returns
#     -------
#
#     '''
#
#     if action == [2,2]:
#         return None
#     elif action[1] == 2:
#
#     elif action[0] == 2:
#         action[0] = 0
#
#     action =


def check_state(state):
    '''

    Parameters
    ----------
    state : list
    The state to be determined whether it is a legal or an illegal move in the environment.

    Returns
    -------
    bool
    Returns True if the state is legal and False otherwise.
    '''
    if state == None:
        return False

    elif state[0][0] < 0 or state[0][1] < 0 or state[1][0] < 0 or state[1][1] < 0: # If there are less than zero shapes on
                                                                                 # either side, return False
        return False
    elif state[0][0] < state[0][1] and state[0][0] != 0:# If the left has less circles than polys and more than zero
                                                      # circles, return False
        return False
    elif state[1][0] < state[1][1] and state[1][0] != 0: # If the right has less circles than polys and more than
                                                         # zero circles, return False
        return False
    else:
        return True


def apply_action(node, action):
    '''
    Applies an action to a given state.

    Parameters
    ----------
    node : Node class
    The node to have the action applied to.

    action : list
    The action to be applied.

    Returns
    -------
    new_node : Node class
    A new node with the applied action
    '''

    import copy

    current_state = node.get_state()
    new_path = copy.copy(node.get_path())

    if node.get_state()[2]:
        num_circles_left = current_state[0][0] + action[0]
        num_polys_left = current_state[0][1] + action[1]
        num_circles_right = current_state[1][0] - action[0]
        num_polys_right = current_state[1][1] - action[1]

    else:
        num_circles_left = current_state[0][0] - action[0]
        num_polys_left = current_state[0][1] - action[1]
        num_circles_right = current_state[1][0] + action[0]
        num_polys_right = current_state[1][1] + action[1]

    new_state = [[num_circles_left, num_polys_left], [num_circles_right, num_polys_right], not current_state[2]]

    if check_state(new_state):
        new_path.append(node)
        new_node = Node(new_state, new_path)
        return new_node

    else:
        return None


def expand(problem, node):
    '''
    Returns a list of nodes that the environment can take as a next step.

    Parameters
    ----------
    problem : Problem class
    A class that contains the current problem.

    node : Node class
    A class the contains the current node.

    Returns
    -------
    new_nodes : list
    A list of the next possible nodes.
    '''
    # apply all possible actions and get the new nodes
    # Return all of the new nodes.
    import copy

    new_nodes = []
    actions = problem.possible_actions
    original_node = copy.copy(node)

    for i in actions:
        new_node = apply_action(original_node, i)
        if new_node != None:
            new_nodes.append(new_node)

    return new_nodes


def breadth_first_search(problem):
    '''
    Returns a solution to the problem or returns failure.
    Parameters
    ----------
    state : list
    The initial state of the environment.

    Returns
    -------
    node : Node class
    A node with state 'goal_state' and the 'path' from the 'problem.initial' to the 'goal_state'.
    '''

    from collections import deque

    node = Node(problem.initial)
    if problem.is_goal(node.state):
        return node
    frontier = [node]
    reached = [problem.initial]
    while frontier: # If something is empty in python, it is False. If not, it is True.
        node = frontier.pop()
        for child in expand(problem, node):
            s = child.state
            if problem.is_goal(s):
                return child
            if s not in reached:
                reached.append(s)
                frontier.append(child)

        # So you want to immediately discard it whenever the polys outnumber the circles.


if __name__ == "__main__":
    initial_state = [[3, 3], [0, 0], False]  # [[circles on left, polys on left],[circles on right, polys on right],
                                     # boolean basketSide]
    goal_state = [[0, 0], [3, 3], True]
    possible_actions = [[0, 0], [1, 0], [2, 0], [0, 1], [0, 2], [1, 1]] # The possible actions from a node
    problem = Problem(initial_state, goal_state, possible_actions)

    solution = breadth_first_search(problem)
    print(solution.get_path())
    for i in solution.get_path():
        print(i.get_state())
    print(solution.get_state())