##
## Library adapted from Berkeley AIMA GSOC
##

from search import *
# ----------------------------------------------------------------------------
# UTIL FUNCTIONS & CLASSES
# ----------------------------------------------------------------------------

class EightPuzzleProblem(Problem):
    '''
    A class for the 8 puzzle problem using the Problem class from search.py.
    '''
    def actions(self, state):
        """For this moveset, r means moving the piece left of the empty space to the right,
        u means moving the piece bellow the empty space up, l means moving the piece left of the space to the right,
        d means moving the piece above the empty space down
        the empty space is represented by a 0
        the entire board is represented by a 9 digit number"""
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
        """This modifies the 9 digit number representing the board based on the action"""
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
# ----------------------------------------------------------------------------

class EightPuzzleNode(Node):
    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state. Also includes the action that got us to this state, and
    the total path_cost (also known as g) to reach the node.
    Use this Class directly, you don't need to subclass it"""
    def solution(self):
        """Return the sequence of actions to go from the root to this node."""
        return [node.action for node in self.path()[1:]] , self.path_cost


from collections import deque

def list_to_int(lst):
    s = [str(i) for i in lst]
    i = int(''.join(s))
    return i

def breadth_first_search(problem):
    current_node = EightPuzzleNode(problem.initial)
    frontier = deque([current_node])
    frontier_sorted = set()
    frontier_sorted.add(list_to_int(current_node.state))
    explored = set()
    notsolved = True
    while notsolved:
        if len(frontier)==0:
            print('failed')
            break
        node = frontier.popleft()
        if node.state == problem.goal:
            print(node.solution())
            break
        explored.add(list_to_int(node.state))
        for action in problem.actions(node.state):
            child = node.child_node(problem, action)
            number = list_to_int(child.state)
            if number not in explored and number not in frontier_sorted:
                frontier.append(child)
                frontier_sorted.add(number)


if __name__ == "__main__":
    start = [7,2,4,5,0,6,8,3,1]
    goal = [0,1,2,3,4,5,6,7,8]

    puzzle = EightPuzzleProblem(start, goal)
    breadth_first_search(puzzle)