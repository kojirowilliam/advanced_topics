


from search import *


class Flatland_Problem(Problem):
    '''
    A class for the Flatland problem using the Problem class from search.py.
    '''
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

        # All of the actions that can occur inside of Flatland at a single step.
        all_actions = [[0, 0], [1, 0], [2, 0], [0, 1], [0, 2], [1, 1]]
        # All of the possible actions that can occur at the given step in Flatland
        possible_actions = [[0,0]]

        if state[2]: # If the basket is on the right, x = -1.
            x = -1
        else:
            x = 1

        for i in all_actions:
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
        The action that has to be performed from the given state.

        Returns
        -------
        new_state : list
        The resultant state from the original state after performing the action.
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


    # def path_cost(self, node):
    #     return len(node.path) # Returns tha cost from getting from the initial state to 'node'.


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
        node = frontier.pop(0)
        for child in node.expand(problem):
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
    problem = Flatland_Problem(initial_state, goal_state)

    BFS_solution = breadth_first_search(problem)

    print(BFS_solution.path())
    print(BFS_solution.solution())
    print(BFS_solution.path_cost)