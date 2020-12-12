from search import *

hueristic = {
    "Oradea": 380,
    "Zerind": 374,
    "Arad": 366,
    "Timisoara": 329,
    "Sibiu": 253,
    "Lugoj": 244,
    "Mehadia": 241,
    "Drobeta": 242,
    "Craiova": 160,
    "Rimnicu": 193,
    "Pitesti": 100,
    "Fagaras": 176,
    "Bucharest": 0,
    "Urziceni": 80,
    "Hirsova": 151,
    "Eforie": 161,
    "Vaslui": 199,
    "Iasi": 226,
    "Neamt": 234
}

class RomaniaProblem(Problem):
    '''
    An abstract class for all of the search methods in the Romania problem.
    '''

    def __init__(self, initial, search_space, goal=None, heuristic=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal. Your subclass's constructor can add
        other arguments."""
        super().__init__(initial, goal)
        self.search_space = search_space
        self.heuristic = heuristic

    def actions(self, state, log=True):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""

        if log:
            print("\tState")
            print("\t\t" + str(state))
            print("\t\t" + str(self.search_space[state]))

            print("\tActions")
            print("\t\t" + str([i[0] for i in self.search_space[state]]))

        return [i[0] for i in self.search_space[state]]

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""

        if action in self.actions(state, False):
            return action

        return NotImplementedError

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal or checks for state in self.goal if it is a
        list, as specified in the constructor. Override this method if
        checking against a single self.goal is not enough."""

        return state == self.goal


class BreadthRomania(RomaniaProblem):
    '''
      Romania problem which implements breadth-first search in terms of path cost
    '''

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2. If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1


class UniformCostRomania(RomaniaProblem):
    '''
    Romania problem which implements uniform-cost search in terms of path cost
    '''

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2. If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""

        for i in self.search_space[state1]:
            if i[0] == state2:
                return i[1] + c

class GreedyBestRomania(RomaniaProblem):
    '''
    Romania problem which implements uniform-cost search in terms of path cost
    '''

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2. If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""

        print("WORKING")

        for i in self.search_space[state1]:
            if i[0] == state2:
                return self.heuristic[i[0]]

# ----------------------------------------------------------------------------
def breadth_first_search(problem):
    '''
    Returns a solution to the problem or returns failure.

    Returns
    -------
    node : Node class
    A node with state 'goal_state' and the 'path' from the 'problem.initial' to the 'goal_state'.
    '''
    loop = 0

    main_node = Node(problem.initial)
    if problem.goal_test(main_node.state):
        return main_node
    frontier = [main_node]
    reached = [problem.initial]
    while frontier:
        loop += 1
        print("Current Frontier: " + str(frontier))
        main_node = frontier.pop(0)
        print("New Node Expansion: " + str(loop))
        print("Popped Frontier: " + str(frontier))
        print("Main Node: " + str(main_node))
        for child in main_node.expand(problem):
            print("\tChild")
            print("\t\t" + str(child))
            s = child.state
            if problem.goal_test(s):
                print("GOAL STATE")
                return child
            if s not in reached:
                print("Not reached, appending")
                reached.append(s)
                frontier.append(child)
        print('. \n.')

def uniform_cost_search(problem):
    '''
    Returns a solution to the problem or returns failure.

    Returns
    -------
    node : Node class
    A node with state 'goal_state' and the 'path' from the 'problem.initial' to the 'goal_state'.
    '''

    loop = 0

    main_node = Node(problem.initial)
    if problem.goal_test(main_node.state):
        return main_node
    frontier = [main_node]
    reached = [problem.initial]
    while frontier:
        loop += 1
        print("Unsorted Frontier: " + str(frontier))
        print([key_path(nodes) for nodes in frontier])
        frontier.sort(key=key_path)
        print("Sorted Frontier: " + str(frontier))
        print([key_path(nodes) for nodes in frontier])
        main_node = frontier.pop(0)
        print("New Node Expansion: " + str(loop))
        print("Popped Frontier: " + str(frontier))
        print("Main Node: " + str(main_node))
        for child in main_node.expand(problem):
            print("\tChild")
            print("\t\t" + str(child))
            s = child.state
            if problem.goal_test(s):
                print("GOAL STATE")
                return child
            if s not in reached:
                print("Not reached, appending")
                reached.append(s)
                frontier.append(child)
        print('. \n.')

def gready_best_first_search(problem):
    '''
    Returns a solution to the problem or returns failure.

    Returns
    -------
    node : Node class
    A node with state 'goal_state' and the 'path' from the 'problem.initial' to the 'goal_state'.
    '''

    loop = 0

    main_node = Node(problem.initial)
    if problem.goal_test(main_node.state):
        return main_node
    frontier = [main_node]
    reached = [problem.initial]
    while frontier:
        loop += 1
        print("Unsorted Frontier: " + str(frontier))
        print([key_path(nodes) for nodes in frontier])
        frontier.sort(key=key_path)
        print("Sorted Frontier: " + str(frontier))
        print([key_path(nodes) for nodes in frontier])
        main_node = frontier.pop(0)
        print("New Node Expansion: " + str(loop))
        print("Popped Frontier: " + str(frontier))
        print("Main Node: " + str(main_node))
        for child in main_node.expand(problem):
            print("\tChild")
            print("\t\t" + str(child))
            s = child.state
            if problem.goal_test(s):
                print("GOAL STATE")
                return child

            if s not in reached:
                reached.append(s)
                frontier.append(child)

                print("Not reached, appending")
        print('. \n.')


def no_comments(problem):
    main_node = Node(problem.initial)
    if problem.goal_test(main_node.state):
        return main_node

    frontier = [main_node]
    reached = [problem.initial]
    while frontier:
        frontier.sort(key=key_path)
        main_node = frontier.pop(0)
        for child in main_node.expand(problem):
            s = child.state

            if problem.goal_test(s):
                return child

            if s not in reached:
                reached.append(s)
                frontier.append(child)


def key_path(child_node):
    return child_node.path_cost


if __name__ == "__main__":
    base_tree = {
        "Oradea": [["Zerind", 71], ["Sibiu", 151]],
        "Zerind": [["Oradea", 71], ["Arad", 75]],
        "Arad": [["Zerind", 75], ["Sibiu", 140], ["Timisoara", 118]],
        "Timisoara": [["Arad", 118], ["Lugoj", 111]],
        "Sibiu": [["Fagaras", 99], ["Rimnicu", 80], ["Arad", 140], ["Oradea", 151]],
        "Lugoj": [["Mehadia", 70], ["Timisoara", 111]],
        "Mehadia": [["Lugoj", 70], ["Drobeta", 75]],
        "Drobeta": [["Craiova", 120], ["Mehadia", 75]],
        "Craiova": [["Pitesti", 138], ["Rimnicu", 146], ["Drobeta", 120]],
        "Rimnicu": [["Pitesti", 97], ["Sibiu", 80], ["Craiova", 146]],
        "Pitesti": [["Craiova", 138], ["Rimnicu", 97], ["Bucharest", 101]],
        "Fagaras": [["Sibiu", 99], ["Bucharest", 211]],
        "Bucharest": [["Urziceni", 85], ["Girugiu", 90], ["Pitesti", 101], ["Fagaras", 211]],
        "Urziceni": [["Hirsova", 98], ["Bucharest", 85], ["Vaslui", 142]],
        "Hirsova": [["Eforie", 86], ["Urziceni", 98]],
        "Eforie": [["Hirsova", 86]],
        "Vaslui": [["Urziceni", 142], ["Iasi", 92]],
        "Iasi": [["Vaslui", 92], ["Neamt", 87]],
        "Neamt": [["Iasi", 87]]
    }

    # solution_breadth = breadth_first_search(BreadthRomania("Arad", base_tree, "Bucharest"))
    # # print(solution_breadth.path)
    #
    # print("\nFINAL PATH:")
    # for nodes in solution_breadth.path():
    #     print(nodes.state)

    solution_uniform = gready_best_first_search(GreedyBestRomania("Arad", base_tree, "Bucharest", hueristic))
    # print(solution_uniform.path)

    print("\nFINAL PATH:")
    for nodes in solution_uniform.path():
        print(nodes.state)


# TODO add distance traveled path

def will_hw6_1():
    print("\nTHE UNVERIFIED CORRECT SOLUTION:")
    print([(i.state, hueristic[i.state]) for i in solution_uniform.path()])
    return ([(i.state, hueristic[i.state]) for i in solution_uniform.path()])

def will_hw6_1():
    print("\nTHE UNVERIFIED CORRECT SOLUTION:")
    print([(i.state, hueristic[i.state]) for i in solution_uniform.path()])
    return ([(i.state, hueristic[i.state]) for i in solution_uniform.path()])

assert will_hw6_1() == [("Arad",366),("Sibiu",253),("Fagaras", 176),("Bucharest",0)]