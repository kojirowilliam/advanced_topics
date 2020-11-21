##
## Library adapted from Berkeley AIMA GSOC
##

from search import *
from search import Node

class Eight_Puzzle_Problem(Node):
    """
    A class for the 8 puzzle problem using the Problem class from search.py.
    """

    def actions(self, state):
        # You're not using action. Try implementing it into
        pos = state.index(0)
        return moveset.moves[pos]

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
            break
        node = frontier.popleft()
        if Problem.goal_test(problem,node):
            print(Node.solution(node))
            break
        explored.add(list_to_int(node.state))
        for action in Problem.actions(problem,node.state):
            child = Node.child_node(node,problem,action)
            number = list_to_int(child.state)
            if number not in explored and number not in frontier_sorted:
                frontier.append(child)
                frontier_sorted.add(number)


if __name__ == "__main__":
    puzzle = Eight_Puzzle_Problem([7,2,4,5,0,6,8,3,1], [0,1,2,3,4,5,6,7,8])
    breadth_first_search(puzzle)