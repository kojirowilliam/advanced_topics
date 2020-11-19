from search import *


class Flatland_Problem(Problem):
    def actions(self, state):
        '''
        Return the actions that can be executed in the given state. The result would typically be a list, but if there
        are many actions, consider yielding them one at a time in an iterator, rather than building them all at once.

        Parameters
        ----------
        state : list
        The current state of Flatland.

        Returns
        -------
        possible_actions : list
        A list of all of the different ways the shapes can be moved in the specified state.
        '''

        all_possible_actions = [[0, 0], [1, 0], [2, 0], [0, 1], [0, 2], [1, 1]]
        possible_actions = [[0,0]]

        if state[2]: # If the basket is on the right, x = -1.
            x = -1

        else:
            x = 1

        for i in all_possible_actions:
            circles_left = state[0][0] - i[0] * x # If the basket is on the right, add instead of subtract.
            polys_left = state[0][1] - i[1] * x # If the basket is on the right, add instead of subtract.
            circles_right = state[1][0] + i[0] * x # If the basket is on the right, subtract instead of add.
            polys_right = state[1][1] + i[1] * x # If the basket is on the right, subtract instead of add.


            if circles_left < 0 or polys_left < 0 or circles_right < 0 or polys_right < 0:  # If there are less than
                                                                            # zero shapes on either side, return False
                pass

            elif circles_left < polys_left and circles_left != 0: # If the left has less circles than polys and more
                                                                  # than zero circles, return False
                pass

            elif circles_right < polys_right and circles_right != 0: # If the right has less circles than polys and more
                                                                     # than zero circles, return False
                pass

            else:
                possible_actions.append(i)

        return possible_actions


    def result(self, state, action):
        '''
        Return the state that results from executing the given action in the given state. The action must be one of
        self.actions(state).

        Parameters
        ----------
        state : list
        The current state of Flatland.

        action : list

        Returns
        -------

        '''

        current_state = state

        if state[2]:  # If the basket is on the right, x = -1.
            x = -1

        else:
            x = 1

        num_circles_left = current_state[0][0] - action[0] * x # If the basket is on the right, add instead of subtract.
        num_polys_left = current_state[0][1] - action[1] * x # If the basket is on the right, add instead of subtract.
        num_circles_right = current_state[1][0] + action[0] * x # If the basket is on the right, subtract instead of add.
        num_polys_right = current_state[1][1] + action[1] * x # If the basket is on the right, subtract instead of add.

        new_state = [[num_circles_left, num_polys_left], [num_circles_right, num_polys_right], not current_state[2]]

        return new_state


    def goal_test(self, state):
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


    def path_cost(self, c, state1, action, state2):
        '''
        Return the cost of a solution path that arrives at state2 from state1 via action, assuming cost c to get up to
        state1. If the problem is such that the path doesn't matter, this function will only look at state2. If the path
        does matter, it will consider c and maybe state1 and action. The default method costs 1 for every step in the
        path.

        Parameters
        ----------
        c
        state1
        action
        state2

        Returns
        -------

        '''

        return c + 1

class Flatland_Node(Node):
    pass


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

    node = Flatland_Node(problem.initial)
    if problem.goal_test(node.state):
        return node
    frontier = [node]
    reached = [problem.initial]
    while frontier: # If something is empty in python, it is False. If not, it is True.
        node = frontier.pop()
        for child in Flatland_Node.expand(problem, node):
            s = child.state
            if problem.goal_test(s):
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
    problem = Flatland_Problem(initial_state, goal_state)

    solution = breadth_first_search(problem)
    print(solution.get_path())
    for i in solution.get_path():
        print(i.get_state())
    print(solution.get_state())