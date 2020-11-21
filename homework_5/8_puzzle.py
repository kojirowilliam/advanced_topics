##
## Library adapted from Berkeley AIMA GSOC
##

import heapq


# ----------------------------------------------------------------------------
# UTIL FUNCTIONS & CLASSES
# ----------------------------------------------------------------------------

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
        pos = state.index(0)
        moves = {
            0: ['u', 'l'],
            1: ['r', 'u', 'l'],
            2: ['r', 'u'],
            3: ['u', 'l', 'd'],
            4: ['r', 'u', 'l', 'd'],
            5: ['r', 'u', 'd'],
            6: ['l', 'd'],
            7: ['r', 'l', 'd'],
            8: ['r', 'd']
        }
        return moves[pos]

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        x=state.index(0)
        newpos = state[:]
        if action == 'r':
            newpos[x] = newpos[x - 1]
            newpos[x - 1] = 0
        if action == 'u':
            newpos[x] = newpos[x + 3]
            newpos[x + 3] = 0
        if action == 'l':
            newpos[x] = newpos[x + 1]
            newpos[x + 1] = 0
        if action == 'd':
            newpos[x] = newpos[x - 3]
            newpos[x - 3] = 0
        return newpos

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2. If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

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
        next_state = problem.result(Problem,self.state, action)
        next_node = Node(next_state, self, action, problem.path_cost(Problem,self.path_cost, self.state, action, next_state))
        return next_node

    def solution(self):
        """Return the sequence of actions to go from the root to this node."""
        return [node.action for node in self.path()[1:]] , self.path_cost

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


from collections import deque

def list_to_int(lst):
    s = [str(i) for i in lst]
    i = int(''.join(s))
    return i

def breadth_first_search(problem):
    current_node = Node(problem.initial)
    frontier = deque([current_node])
    frontier_sorted = set()
    frontier_sorted.add(list_to_int(current_node.state))
    explored = set()
    notsolved = True
    while notsolved:
        if len(frontier)==0:
            print('failed')
            notsolved = False
            break
        node = frontier.popleft()
        if node.state == problem.goal:
            print(Node.solution(node))
            notsolved = False
            break
        explored.add(list_to_int(node.state))
        for action in Problem.actions(problem,node.state):
            child = Node.child_node(node,problem,action)
            number = list_to_int(child.state)
            if number not in explored and number not in frontier_sorted:
                frontier.append(child)
                frontier_sorted.add(number)

puzzle = Problem
start = [7,2,4,5,0,6,8,3,1]
goal = [0,1,2,3,4,5,6,7,8]
puzzle.__init__(Problem, start, goal)
breadth_first_search(puzzle)