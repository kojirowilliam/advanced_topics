class Agent():
    def __init__(self, percept):
        self.percept = percept
        rule(percept)

    def rule(self):

        # Agent doesn't move, but tells the environment to move the agent in the environment.
        pass
