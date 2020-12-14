def is_in(elt, seq):
    """ test if elt is in sequence, seq using is instead of =="""
    # list comprehension [x is elt for x in seq] ;
    # generator expression (x is elt for x in seq)
    return any( x is elt for x in seq)


class Problem:
    """The abstract class for a formal problem. You should subclass
    this and implement the methods actions and result, and possibly
    __init__, goal_test, and path_cost. Then you will create instances
    of your subclass and solve them with the various search functions."""

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal. Your subclass's constructor can add
        other arguments."""
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        raise NotImplementedError

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        raise NotImplementedError

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal or checks for state in self.goal if it is a
        list, as specified in the constructor. Override this method if
        checking against a single self.goal is not enough."""
        if isinstance(self.goal, list):
            return is_in(state, self.goal)
        else:
            return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2. If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1


class Node:
    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state. Also includes the action that got us to this state, and
    the total path_cost (also known as g) to reach the node.
    Use this Class directly, you don't need to subclass it"""

    def __init__(self, next_state=None, parent=None, action=None, path_cost=None, problem=None):
        """Create a search tree Node, derived from a parent by an action."""
        if next_state:
            self.state = next_state
        else:
            self.state = problem.initial
        self.parent = parent
        self.action = action
        if path_cost:
            self.path_cost = path_cost
        else:
            self.path_cost = problem.path_cost(0, self.state, action, None)
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
        print(f"{self} path cost is {self.path_cost}")
        next_node = Node(next_state, self, action, problem.path_cost(self.path_cost, self.state, action, next_state), problem)
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

romania_map = {
    "Arad" : {"Zerind" : 75, "Sibiu" : 140, "Timisoara" : 118},
    "Bucharest" : {"Urziceni" : 85, "Pitesti" : 101, "Giurgiu" : 90, "Fagaras" : 211},
    "Craiova" : {"Drobeta" : 120, "Rimnicu" : 146, "Pitesti" : 138},
    "Drobeta" : {"Mehadia" : 75, "Craiova": 120},
    "Eforie" : {"Hirsova" : 86},
    "Fagaras" : {"Sibiu" : 99, "Bucharest": 211},
    "Giurgiu" : {"Buchareset": 90},
    "Hirsova" : {"Urziceni" : 98, "Eforie" : 86},
    "Iasi" : {"Vaslui" : 92, "Neamt" : 87},
    "Lugoj" : {"Timisoara" : 111, "Mehadia" : 70},
    "Mehadia" : {"Lugoj" : 70, "Drobeta" : 75},
    "Neamt" : {"Iasi" : 87},
    "Oradea" : {"Zerind" : 71, "Sibiu" : 151},
    "Pitesti" : {"Rimnicu" : 97, "Bucharest" : 101},
    "Rimnicu" : {"Sibiu" : 80, "Pitesti" : 97, "Craiova" : 146},
    "Sibiu" : {"Rimnicu" : 80, "Fagaras" : 99, "Oradea" : 151, "Arad" : 140 },
    "Timisoara" : {"Arad" : 118, "Lugoj" : 111},
    "Urziceni" : {"Vaslui" : 142, "Bucharest" : 85, "Hirsova" : 98},
    "Vaslui" : {"Iasi" : 92, "Urziceni" : 142},
    "Zerind" : {"Oradea" : 71, "Arad" : 75}
}


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
    "Neamt": 234,
    "Girugiu": 77
}
# ----------------------------------------------------------------------------


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


class GreedyBestRomania(RomaniaProblem):
    '''
    Romania problem which implements uniform-cost search in terms of path cost
    '''

    def path_cost(self, c, state1, action, state2=None):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2. If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""

        if state2 is not None:
            for i in self.search_space[state1]:
                if i == state2:
                    return self.heuristic[i[0]]
        else:
            return self.heuristic[state1]


class AStarRomania(RomaniaProblem):
    '''
    Romania problem which implements uniform-cost search in terms of path cost
    '''

    def path_cost(self, c, state1, action, state2=None):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2. If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        if state2 is not None:
            for i in self.search_space[state1]:
                if i[0] == state2:
                    return i[1] + c
        else:
            return 0


def search(problem):
    '''
    Returns a solution to the problem or returns failure.

    Returns
    -------
    node : Node class
    A node with state 'goal_state' and the 'path' from the 'problem.initial' to the 'goal_state'.
    '''

    loop = 0

    main_node = Node(problem.initial, None, None, None, problem)
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
        if problem.goal_test(main_node.state):
            print("GOAL STATE")
            return main_node
        for child in main_node.expand(problem):
            print("\tChild")
            print("\t\t" + str(child))
            print("\t\t" + str(child.path_cost + hueristic[str(child.state)]))
            s = child.state

            if s not in reached or (s in reached and problem.goal_test(s)):
                reached.append(s)
                frontier.append(child)

                print("Not reached, appending")
        print('. \n.')


def key_path(child_node):
    return child_node.path_cost + hueristic[str(child_node.state)]

def will_hw6_1():
    solution_greedy = search(GreedyBestRomania("Arad", base_tree, "Bucharest", hueristic))
    print("\nTHE UNVERIFIED CORRECT SOLUTION:")
    path = solution_greedy.path()
    solution = [(i.state, hueristic[i.state]) for i in path]
    print(solution)
    print("\nDISTANCE TRAVELED:")
    distance = 0
    if len(path) > 0:
        for i in range(len(path) - 1):
            distance += romania_map[path[i].state][path[i+1].state]
    print(f"From Arad to Bucharest is {distance}")
    return solution


def will_hw6_2():
    solution_astar = search(AStarRomania("Arad", base_tree, "Bucharest", hueristic))
    print("\nTHE UNVERIFIED CORRECT SOLUTION:")
    path = solution_astar.path()
    solution = [(i.state, i.path_cost + hueristic[str(i.state)]) for i in path]
    print(solution)
    print("\nDISTANCE TRAVELED:")
    distance = 0
    if len(path) > 0:
        for i in range(len(path) - 1):
            distance += romania_map[path[i].state][path[i + 1].state]
    print(f"From Arad to Bucharest is {distance}")
    return solution


if __name__ == "__main__":
    assert will_hw6_1() == [('Arad', 366), ('Sibiu', 253), ('Fagaras', 176), ('Bucharest', 0)]
    assert will_hw6_2() == [("Arad", 366), ("Sibiu", 393), ("Rimnicu", 413), ("Pitesti", 417), ("Bucharest", 418)]



