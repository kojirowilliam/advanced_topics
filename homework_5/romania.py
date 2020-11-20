
# ----------------------------------------------------------------------------
# UTIL FUNCTIONS & CLASSES

def is_in(elt, seq):
    """ test if elt is in sequence, seq using is instead of =="""
    # list comprehension [x is elt for x in seq] ;
    # generator expression (x is elt for x in seq)
    return any(x is elt for x in seq)

"""
        for i in self.connections(state):
            if action in i:
                return i[1]

        return NotImplementedError
"""

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

# ----------------------------------------------------------------------------


class Queue:

    def __init__(self, values=[]):
        self.values = values

    def push(self, addition):
        # self.values = self.values.append(addition)
        self.values = self.values.extend(addition)

    def pop(self):
        self.values = self.values.pop()

    def __repr__(self):
        """proxy to the representation for heapq"""
        return self.values.__repr__()

# ----------------------------------------------------------------------------


class Problem:
    """The abstract class for a formal problem. You should subclass
    this and implement the methods actions and result, and possibly
    __init__, goal_test, and path_cost. Then you will create instances
    of your subclass and solve them with the various search functions."""

    def connections(self, state):
        return self.tree[state]

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""

        for i in self.connections(state):
            return i[0]

        return NotImplementedError

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""

        if action in self.actions(state):
            return action

        return NotImplementedError


class BreadthRomania(Problem):

    def __init__(self, initial, search_space, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal. Your subclass's constructor can add
        other arguments."""
        self.initial = initial
        self.goal = goal
        self.tree = search_space

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2. If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal or checks for state in self.goal if it is a
        list, as specified in the constructor. Override this method if
        checking against a single self.goal is not enough."""
        if isinstance(self.goal, list):
            return is_in(state, self.goal)
        else:
            return state == self.goal



# ----------------------------------------------------------------------------


class Node:
    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state. Also includes the action that got us to this state, and
    the total path_cost (also known as g) to reach the node.
    Use this Class directly, you don't need to subclass it"""

    def __init__(self, state, parent=None, action=None, path_cost=0):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node {}>".format(self.state)

    def __lt__(self, node):
        return self.state < node.state

    def expand(self, problem):
        """List the nodes reachable in one step from this node."""
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        """return the child node that results from applying action"""
        next_state = problem.result(self.state, action)
        next_node = Node(next_state, self, action, problem.path_cost(self.path_cost, self.state, action, next_state))
        return next_node

    def solution(self):
        """Return the sequence of actions to go from the root to this node."""
        return [node.action for node in self.path()[1:]]

    def path(self):
        """Return a list of nodes forming the path from the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    def __eq__(self, other):
        """Node are equal if they have the same class and their states are equal. This may have to be
        overridden if the state equality can not be determined from =="""
        return isinstance(other, Node) and self.state == other.state


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

    main_node = Node(problem.initial)
    if problem.goal_test(main_node.state):
        return main_node
    frontier = [main_node]
    reached = [problem.initial]
    while frontier:
        main_node = frontier.pop()
        for child in main_node.expand(problem):
            s = child.state
            if problem.goal_test(s):
                return child
            if s not in reached:
                reached.append(s)
                frontier.append(child)


if __name__ == "__main__":
    solution = breadth_first_search(BreadthRomania("Arad",  "Bucharest"))
    print(solution.get_path())
    for nodes in solution.get_path():
        print(nodes.get_state())
    print(solution.get_state())