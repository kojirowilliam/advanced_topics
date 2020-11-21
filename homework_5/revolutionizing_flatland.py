


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
        possible_actions = []

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

        if state == self.goal:
            return True
        else:
            return False


class Flatland_Node(Node):
    '''
    A class that represents a node (instance of the Flatland Environment) using the Node class from search.py.
    '''

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
    A node with state 'goal_state' and the 'path' containing both the 'problem.initial' and the 'goal_state'.
    '''

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


def tests():
    '''
    Tests the functions inside of revolutionizing_flatland.py.
    '''

    test_problem = Flatland_Problem([[3, 3], [0, 0], False], [[0, 0], [3, 3], True])

    # Testing Flatland_Problem().actions()
    actions = test_problem.actions([[3, 3], [0, 0], False])
    correct_actions = [[0,0], [0, 1], [0, 2], [1, 1]]
    assert(actions == correct_actions), "Failed initial test for Flatland_Problem.actions(state). Predicting " \
                                        "incorrect actions."
    actions = test_problem.actions([[2, 2], [1, 1], False])
    correct_actions = [[0, 0], [2, 0], [1, 1]]
    assert (actions == correct_actions), "Failed practical test for Flatland_Problem.actions(state). Inaccurate " \
                                         "prediction of possible actions."
    actions = test_problem.actions([[3, 0], [0, 3], False])
    correct_actions = [[0,0]]
    assert (actions == correct_actions), "Failed impossible test for Flatland_Problem.actions(state). Predicted an " \
                                         "impossible action."

    # Testing Flatland_Problem().result()
    all_actions = [[0, 0], [1, 0], [2, 0], [0, 1], [0, 2], [1, 1]]
    # correct_results = []
    # for i in all_actions:
    #     correct_results.append(test_problem.result([[0, 0], [3, 3], True], i))
    # print(correct_results)

    correct_results = [[[3, 3], [0, 0], True], [[2, 3], [1, 0], True], [[1, 3], [2, 0], True],
                       [[3, 2], [0, 1], True], [[3, 1], [0, 2], True], [[2, 2], [1, 1], True]]
    actions = [[0, 0], [1, 0], [2, 0], [0, 1], [0, 2], [1, 1]]
    results = []
    for i in actions:
        results.append(test_problem.result([[3, 3], [0, 0], False], i))
    assert(results == correct_results), "Failed initial state test for Flatland_Problem.results(state). Incorrect " \
                                        "calculations of the resulting actions."

    correct_results = [[[0, 0], [3, 3], False], [[1, 0], [2, 3], False], [[2, 0], [1, 3], False],
                       [[0, 1], [3, 2], False], [[0, 2], [3, 1], False], [[1, 1], [2, 2], False]]
    actions = [[0, 0], [1, 0], [2, 0], [0, 1], [0, 2], [1, 1]]
    results = []
    for i in actions:
        results.append(test_problem.result([[0, 0], [3, 3], True], i))
    assert(results == correct_results), "Failed other side initial state test for Flatland_Problem.results(state). " \
                                        "Incorrect calculations of the resulting actions."

    # Testing Flatland_Problem().goal_test()
    assert(not test_problem.goal_test([[0, 2], [3, 1], False])), "A non-goal_state state returned True from goal_test"
    assert(not test_problem.goal_test([[0, 0], [3, 3], False])), "Basket is on the wrong side, yet goal_test returned" \
                                                                  "True"
    assert(test_problem.goal_test([[0, 0], [3, 3], True])), "goal_test returned False when it should have returned True"

    # Testing Node().expand() and Node.child_node()
    test_node = Node([[3, 3], [0, 0], False])
    expanded_test_node = test_node.expand(test_problem)
    correct_expanded_test_node_states = [[[3, 3], [0, 0], True], [[3, 2], [0, 1], True], [[3, 1], [0, 2], True],
                                         [[2, 2], [1, 1], True]]

    for i,v in enumerate(expanded_test_node):
        assert(v.state == correct_expanded_test_node_states[i])

    print("All tests passed. Everything's working properly!\n")



if __name__ == "__main__":

    # States are represented as [[circles on left, polys on left],[circles on right, polys on right],boolean basketSide]
    tests()
    initial_state = [[3, 3], [0, 0], False]
    goal_state = [[0, 0], [3, 3], True]
    problem = Flatland_Problem(initial_state, goal_state)

    BFS_solution = breadth_first_search(problem)

    print("The solution path with BFS:\n", BFS_solution.path())
    print("The solution actions with BFS:\n", BFS_solution.solution())
    print("The total path cost with BFS:\n", BFS_solution.path_cost)