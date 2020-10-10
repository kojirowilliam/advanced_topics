from random import randint

class Agent:
    '''
    A class that represents an Agent in the Environment.

    ...

    Attributes
    ----------
    percepts : list
        tells whether the agent is in the left room and whether the room it's currently in is clean.

    Methods
    -------
    set_percepts(agent_percepts)
        sets the agent's perception of the environment.
    rules()
        returns an action based on the perception of the environment from the perspective of the agent.
    '''

    def __init__(self, percepts=None):
        '''
        Parameters
        ----------
        percepts : list
            a list of strings and/or Nones representing the perception of the environment from the perspective of
            the agent.
        performance : int
            an integer representing the number of times the agent has completed a task.
        '''

        self.percepts = percepts
        self.performance = 0

    def set_percepts(self, agent_percepts):
        '''
        Sets the agent's perception of the environment.

        Parameters
        ----------
        percepts : list
            A list of strings and/or Nones that represents the environment from the Agent's perceptions
        '''

        self.percepts = agent_percepts

    def rules(self):
        '''
        Returns an action depending on the agent's perceptions of the environment.

        Returns
        -------
        action : str
            a string representing the action the Agent wants to make in the environment.
        '''
        if "cleaned" in self.percepts:
            self.performance += 1
        if "clean" in self.percepts:
            action = "suck"
        else:
            if "left" in self.percepts:
                action = "right"
            else:
                action = "left"
        return action


class Vacuum_Environment:
    """
    A class representing one clean room and one dirty room for a vacuum agent.

    ...

    Attributes
    ----------
    world : list
        an integer list representing the two rooms and the agent: A agent is represented with a 1 and the empty room
        with a 0.
    dirty_room : list
        an integer list representing the two rooms: a clean room is represented with a 0 and a dirty room is represented
        with a 1.
    agent_action : str
        the action the agent will do in the environment.
    environment_won : bool
        Keeps track of whether the environment it is currently in is already won.
    score : int
        Keeps track of the number of times the agent has completed the environments' tasks.

    Methods
    -------
    create_world()
        Sets the 'world' class variable representing the rooms of the environment and agent inside of it.

    create_dirt()
        Sets the 'dirty_room' class variable representing the clean and dirty room inside of it.

    agent_program(agent)
        Makes the object agent's percepts and sets that inside of the agent. Then, it calls agent.rules() to get the
        agent's action and sets that equal to the 'agent_action' class variable.

    change_environment()
        Changes the state of the environment based on the agent_action class variable.

    get_dirt_status()
        Getter for the status of the dirty room in the environment.

    __repr__()
        Represents the class when printed as a formatted string of the 'world' class variable and 'dirty_room' class
        variable.
    """

    def __init__(self):
        '''
        Parameters
        ----------
        world : list
            an integer list representing the two rooms and the agent: A agent is represented with a 1 and the empty room
            with a 0.
        dirty_room : list
            an integer list representing the two rooms: a clean room is represented with a 0 and a dirty room is
            represented with a 1.
        agent_action : str
            the action the agent will do in the environment.
        environment_won : bool
            Keeps track of whether the environment it is currently in is already won.
        score : int
            Keeps track of the number of times the agent has completed the environments' tasks.
        '''

        self.world = []
        self.dirty_room = []
        self.agent_action = ""
        self.environment_won = False
        self.score = 0

    def create_world(self):
        '''
        Sets the 'world' class variable representing the rooms of the environment and agent inside of it.
        The 'world' class variable represents the location of the agent and the room that it is in.

        Raises
        ------
        AttributeError
            If there is already a pre-existing 'world', this will prevent overriding it with a new 'world'.
        '''

        if self.world == []:
            world = randint(0, 1)
            if world:
                self.world = [0, 1]
            else:
                self.world = [1, 0]
        else:
            raise AttributeError("Can't create new world. Pre-existing world exists!")

    def create_dirt(self):
        '''
        Sets the 'dirty_room' class variable representing clean rooms with 0 and dirty rooms with 1 inside of the environment.
        The 'dirty_room' class variable represents the location of the dirty room with a 1 and the clean room with a 0.

        Raises
        ------
        AttributeError
            If there is already a pre-existing 'dirty_room', this will prevent overriding it with a new 'dirty_room'.
        '''

        if self.dirty_room == []:
            self.dirty_room = [randint(0, 1), randint(0, 1)]
        else:
            raise AttributeError("Can't create new dirt. Pre-existing dirt exists!")

    def agent_program(self, agent):
        '''
        Makes the object agent's percepts and sets that inside of the agent. Then, it calls agent.rules() to get the
        agent's action and sets that equal to the 'agent_action' class variable.

        Parameters
        ----------
        agent : Object of Agent class
        '''

        agent_percepts = []

        if self.get_dirt_status() == [] and self.environment_won == False:
            agent_percepts.append("cleaned")
            self.environment_won = True
        if self.world == [1, 0]:
            agent_percepts.append("left")
        else:
            agent_percepts.append(None) # Appending None to emphasize the agent's lack of intelligence
        if 1 in self.dirty_room and self.dirty_room[self.world.index(1)] == 1:
            agent_percepts.append("clean")
        else:
            agent_percepts.append(None) # Appending None to emphasize the agent's lack of intelligence
        agent.set_percepts(agent_percepts)
        self.agent_action = agent.rules()
        print(self.agent_action)

    def change_environment(self):
        '''
        Changes the state of the environment based on the agent_action class variable.
        If the dirty room becomes clean, the 'dirty_room' class variable becomes an empty list since there are no more
        dirty rooms in the environment.

        Raises
        ------
        NotImplementedError
            If the 'agent_action' is an empty string, that means that the agent isn't doing anything. For this agent,
            this isn't a support action.
        '''

        if self.agent_action != "":
            if self.agent_action == "suck" and 1 in self.dirty_room and self.dirty_room[self.world.index(1)] == 1:
                self.dirty_room[self.world.index(1)] = 0
                self.score += 1
            if self.agent_action == "left":
                self.world = [1, 0]
            elif self.agent_action == "right":
                self.world = [0, 1]
        else:
            raise NotImplementedError("The agent is taking no action! No action is not supported!")

    def get_dirt_status(self):
        '''
        Getter for the status of the dirty room in the environment.

        Returns
        -------
        dirty_room : list
            an integer list representing the two rooms: a clean room is represented with a 0 and a dirty room is
            represented with a 1.
        '''

        return self.dirty_room

    def __repr__(self):
        '''
        Represents the class when printed as a formatted string of the 'world' class variable and 'dirty_room' class
        variable.

        Returns
        -------
        str
            an formatted string representing the 'world' class variable and 'dirty_room' class variable.
        '''

        return f"world = {self.world}, dirty_room = {self.dirty_room}"


if __name__ == '__main__':
    '''
    The main loop of the program.

    Variables
    ----------
    total_score : int
        The number of times the agent has completed the environment (has cleaned the dirty room).
    steps_max : int
        The number of steps the environment will take to complete the program.
    steps : int
        Keeps track of the number of steps the environment takes.
    run : bool
        Keeps track of when the environment is running and when it has stopped.
    vacuum_world : Object
        An object from the Vacuum_Environment() class
    roomba : Object
        An object from the Agent() class
    '''

    total_score = 0
    step_max = 10
    steps = 1
    run = True
    vacuum_world = Vacuum_Environment()
    vacuum_world.create_world()
    vacuum_world.create_dirt()
    print(vacuum_world)
    roomba = Agent()
    while run:
        steps += 1
        if steps == step_max:
            run = False
        vacuum_world.agent_program(roomba)
        vacuum_world.change_environment()
        print(vacuum_world)

    total_score = vacuum_world.score
    if total_score > 0:
        print(f"\nThe roomba has completed the task(s) in the environment(s) {total_score} times.")
    else:
        print("\nThe roomba has not completed the task(s) in the environment.")