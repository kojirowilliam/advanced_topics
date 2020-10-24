from abc import ABC, abstractmethod
from random import randint
import logging

from hw4_util import Tile

from hw4_util import read_world
from yamada_world import yamada, deer, catalan, churchland, meister, depue

def setup_logging(level):
    logging.basicConfig(level=0, format='%(asctime)s{%(levelname)s} %(message)s', datefmt='%H:%M:%S')

# shorthand convenience methods for using logger
global debug, warn, info, error, crash
debug = logging.debug
info = logging.info
warn = logging.warning
error = logging.error
crash = logging.critical

# initialize logger
# debug and warn messages will be skipped
setup_logging(logging.WARNING)

# the first definition is the last cardinal direction that the agent moved, this is where the agent is "facing"
# the second dictionary defines what this means for the relative actions of the agent,
# for example, if you're facing down and take a right, that's going left in world directions
movement_decrypt = {
    "right": {"right": "down", "left": "up", "forward": "right", "back": "left"},
    "left": {"right": "up", "left": "down", "forward": "left", "back": "right"},
    "up": {"right": "right", "left": "left", "forward": "up", "back": "down"},
    "down": {"right": "left", "left": "right", "forward": "down", "back": "up"}
}

# this converts cardinal movements to vectors
string_movement_to_vector = {
    "right": [0, 1],
    "left": [0, -1],
    "up": [-1, 0],
    "down": [1, 0],
    "suck": [-99, -99]  # should throw error
}

class Agent(ABC):
    '''
    An abstract class that represents a roomba Agent for the Vacuum Environments.
    ...
    Attributes
    ----------
    percepts : list
        A list of strings that represent all of the percepts the agent has had. The last two percepts are the current
        percepts of the agent.
    performance : integer
        An integer representing the number of times the agent has completed a task.
    action : string
        A string representing the current action the agent is going to take.
    Methods
    -------
    set_percepts(agent_percepts)
        sets the agent's perception of the environment as the class variable 'percepts'
    rules()
        returns an action based on the perception of the environment from the perspective of the agent.
    '''

    def __init__(self, percepts=None):
        '''
        Parameters
        ----------
        percepts : list
            A string list of the history of perceptions from the agent from the environment. The last strings on the
            list are the current percepts of the agent.
        '''
        self.percepts = percepts
        self.performance = 0
        self.action = "right"


    def set_percepts(self, agent_percepts):
        '''
        Sets the percepts class variable of the environment.
        Parameters
        ----------
        percepts : list
            A list of strings that represents the history of perceptions from the Agent's perspective of the environment
        '''
        self.percepts = agent_percepts


    @abstractmethod
    def rules(self):
        pass

class Toyota_Corolla_Agent(Agent):
    '''
    A class that represents our first Reflex Agent in the Environment.
    ...
    Attributes
    ----------
    percepts : list
        tells whether the agent has bumped into a wall, whether the ground/wall is clean
    Methods
    -------
    agent_type()
        returns agent name, used for agent movement types
    rules()
        returns an action based on the perception of the environment from the perspective of the agent.
    '''

    def agent_type(self):
        '''
        Returns the type of agent.

        Returns
        -------
            str

        '''
        return "Reflex_Agent"

    def rules(self):
        '''
        Returns an action depending on the agent's perceptions of the environment.
        How our rules work is such:
        We're always sticking to the right, so the first thing we ALWAYS do is try to move right.
        If we tried to move right last action, and we got back a bump in our percept, let's try to move Forward, etc.
        Right -> Forward -> Left -> Back

        All the agent knows how to do is see if it bumped, then it chooses a new movement,
                                        or it isn't bumped, so it moves right

        Remember, these are relative movements, the roomba doesn't know which way is up or down.
        The enviornment knows which way the Roomba is pointing however.
        The way the roomba is pointing and it's action is decryrpted by the enviornment.
        This allows us to stick to the right, even when we're facing left, down, up, or right.
        We always move to the relative right.

        Returns
        -------
        action : str
            a string representing the action the Agent wants to make in the environment.
        '''

        rules_dict = {
            # this is the sequential order of moves in relative roomba space. directions are relative to where roomba is
            # looking, not cardinal environment directions
            "right": "forward",
            "forward": "left",
            "left": "back",
            "back": "error"
        }

        reverse_dict = {
            # this makes the roomba turn around
            # turning around means the roomba's old left is not its right, meaning it will try to stick to a wall that's across from it
            "right": "left",
            "forward": "back",
            "left": "right",
            "back": "forward",
            "suck": "right"
        }

        dirt_percept = self.percepts[-2]
        bump_percept = self.percepts[-1]
        print("-     Agent's POV     -")
        print(f"Dirt Percept: {dirt_percept}")
        print(f"Bump Percept: {bump_percept}")
        print(f"Last Action: {self.action}")

        if dirt_percept == "dirty":  # if dirty
            print("IM SUCKING SUCKING SUCKING SUCKING ")
            self.action = "suck" # suck
            self.performance += 1 # update your personal score
        else:
            if bump_percept == "bump":  # okay, we tried to move and we hit something, let's take our last action and use it to find a new one
                self.action = rules_dict.get(self.action)
                print("We Bumped - DICTIONARY ACTION")
                print(self.action)
            else:  # we haven't bumped into anything, so try to move right
                print("Not Bumped - NORMAL ACTION")
                if randint(0, 100) < 5 : # random case to help us get to harder-to-reach areas
                    # self.action = "right"
                    self.action = reverse_dict.get(self.action) # turn around and try to attach to a inside/outside wall
                else:
                    self.action = "right"

                print(self.action)

            if self.action == "error":  # we've tried to move everywhere and nothing worked, throw error
                raise AttributeError("Roomba is stuck in a hole, no possible movements")

        return self.action

class Simple_Agent(Agent):
    '''
    A class that represents our second Reflex Agent in the Environment.
    We were scared that our first reflex agent was using too much information (even
    ...
    Attributes
    ----------
    percepts : list
        tells whether the agent has bumped into a wall, whether the ground/wall is clean
    Methods
    -------
    agent_type()
        returns agent name, used for agent movement types
    rules()
        returns an action based on the perception of the environment from the perspective of the agent.
    '''

    def agent_type(self):
        return "Simple_Agent"

    def rules(self):
        '''
        Returns an action depending on the agent's perceptions of the environment.
        How our rules work is such:
        This is the simple agent, in case Spell doesn't like what we're doing with our Reflex Agent
        All it does is always turn left if bumped, forward if not.
        I threw some randomness in there to help it out.
        There's no action sequence here, unlike the other bot.
        This one can get stuck much easier.

        Returns
        -------
        action : str
            a string representing the action the Agent wants to make in the environment.
        '''

        dirt_percept = self.percepts[-1][-1]
        bump_percept = self.percepts[-1][-2]

        if dirt_percept == "dirty":  # duh
            self.action = "suck"
            self.performance += 1
        else:  # if we haven't tried to move yet, let's move right
            if bump_percept == "bump":  # okay, we tried to move and we hit something, let's take our last action and use it to find a new one
                if randint(0, 100) < 5:
                    self.action = "right"
                else:
                    self.action = "left"
            else:
                self.action = "forward"

        return self.action

class Model_Agent(Agent):
    '''
    A class that represents an Agent in the Environment.
    ...
    Attributes
    ----------
    percepts : list
        tells whether the agent has bumped into a wall, whether the ground/wall is clean
    Methods
    -------
    agent_type()
        returns agent name, used for agent movement types
    rules()
        returns an action based on the perception of the environment from the perspective of the agent.
    mapping()
        tries to construct a roomba based understanding of the enviornmetn
    virtual bump check()
        checks if agent will virtually bump into a virtual wall
    virtual_rules()
        runs the rules function recursively to find rules that apply to virtual worlds
    '''
    def __init__(self):
        self.world=[]
        self.agent_col=0
        self.agent_row=0
        self.prepmap(6, 7)
        self.agent_last_successful = "right"
        self.cardinal_action = "right"
        self.antiloop = []  # list to be used to monitor whether the agent is stuck in a loop
        super().__init__()

    def agent_type(self):
        return "Model_Agent"

    def prepmap(self, x, y):
        '''
        Prepares the list that will contain the map for mapping to begin.
        Relies on the starting dimensions of the world to make a filler list
        that will be guaranteed to contain the world no matter where the agent starts.

        Parameters
        ----------
        x
        y

        Returns
        -------
        2d array of '-' with dimensions sufficient to contain the environment
        '''
        row = list('-' * ((2 * x) - 1))
        for i in range(((2 * y) - 1)):
            self.world.append(row[:])
        self.agent_col = x - 1
        self.agent_row = y - 1
        return self.world

    def interpret_cardinal_action(self):
        '''
        Converts the relative actions that the agent outputs into cardinal actions for the mapping function
        Returns
        -------
        cardinal direction, string
        '''
        if self.action != "suck":
            self.cardinal_action = str(movement_decrypt[self.agent_last_successful][self.action])

    def mapping(self, agent_percepts):
        '''agent tries to construct a map of the world based on past experience'''
        if self.cardinal_action == "right":  # agent moves right
            if agent_percepts[1] != "bump":  # agent has not ran into a wall
                self.agent_col += 1  # collumn variable changed
                self.world[self.agent_row][self.agent_col] = 1  # agent's new square marked as empty
            if agent_percepts[1] == "bump":  # agent has ran into wall
                self.world[self.agent_row][self.agent_col + 1] = 2  # square to the right of the agent marked as wall
        if self.cardinal_action == "left":  # agent moves left
            if agent_percepts[1] != "bump":  # agent has not ran into wall
                self.agent_col -= 1  # collumn variable changed appropriately
                self.world[self.agent_row][self.agent_col] = 1  # agent's new position marked as empty
            if agent_percepts[1] == "bump":  # agent has hit a wall
                self.world[self.agent_row][self.agent_col - 1] = 2  # square to the left of agent marked as wall
        if self.cardinal_action == "up":  # agent moves up
            if agent_percepts[1] != "bump":  # agent has not hit a wall
                self.agent_row -= 1  # row variable decreased
                self.world[self.agent_row][self.agent_col] = 1  # agent's new position marked as empty
            if agent_percepts[1] == "bump":  # agent has encountered a wall
                self.world[self.agent_row - 1][self.agent_col] = 2  # square directly above agent marked as wall
        if self.cardinal_action == "down":  # agent moves down
            if agent_percepts[1] != "bump":  # agent does not hit wall
                self.agent_row+=1
                self.world[self.agent_row][self.agent_col] = 1
            if agent_percepts[1] == "bump":  # agent has encountered wall
                self.world[self.agent_row + 1][self.agent_col] = 2  # square directly below agent marked as wall

    def get_pos_value(self, x, y):
        '''
        This checks the value of a given square in the world (relative to starting position)
        Parameters
        ----------
        x
        y

        Returns
        -------
        -,0,1,2,3
        '''
        return self.world[x][y]

    def has_visited(self, x, y):
        '''
        Checks whether the agent has visited a certain square
        Parameters
        ----------
        x
        y

        Returns
        -------
        True/False
        '''
        if self.world[x][y] != '-':
            return True
        else:
            return False

    def loop_tracker(self):
        '''
        Watches for possible loops the agent could be stuck in
        Returns
        -------
        True/False
        '''
        coords = [self.agent_row, self.agent_col]  # coordinates of agent
        if self.has_visited(coords[0], coords[1]):
            if self.antiloop.count([coords]) >= 3:  # method of tracking loops only works if agent has visited a square at least 3 times
                loop_spots = [i for i in range(len(self.antiloop)) if self.antiloop[i] == [coords]][-2:]  # makes list of indexes of every time the agent has previously been in its current square (only takes the last 2 as only 2 are needed)
                if self.antiloop[loop_spots[0] + 1] == self.antiloop[loop_spots[1] + 1]:  # if the move directly after each of the previous visits is the same then the agent might be stuck in a loop
                    self.antiloop = []  # list keeping track of previous positions is wiped so the previous if/else statements don't keep checking the same occurences
                    return True
                else:
                    self.antiloop = []  # list keeping track is wiped for the same reason
                    self.antiloop.append([coords])  # current coordinates are appended
                    return False
            else:
                self.antiloop.append([coords])  # if agent has not visited a given square at least 3 times its current position is added to list

    def rules(self):
        '''
        Returns an action depending on the agent's perceptions of the environment.
        How our rules work is such:
        We're always sticking to the right, so the first thing we ALWAYS do is try to move right.
        If we tried to move right last action, and we got back a bump in our percept, let's try to move Forward, etc.
        Right -> Forward -> Left -> Back
        But this agent is MUCH SMARTER than the last one because we now can maintain state of the world.
        What we're doing now is trying to spiral around the world until we reach the inside.
        In order to spiral inwards, we need to pretend like there's blocks in certain spaces : "Virtual Walls"
        These Virtual Walls should impede our movement, but they don't exist in the environment, the enviornment has no
        idea about them

        What we're doing here is doing our normal movement code, then checking if that movement will cause a bump into
        our Virtual Walls.

        If that movement will make us go into a virtual wall, we send it back to regenerate, making the rules think we
        just bumped into something and it's the next step, but it isn't
        This creates the recursive nature of our virtual code.
        Remember, these are relative movements, the roomba doesn't know which way is up or down.
        The enviornment knows which way the Roomba is pointing however. The way the roomba is pointing and it's action
        is decryrpted by the enviornment.

        This allows us to stick to the right, even when we're facing left, down, up, or right. We always move to the
        relative right.
        Returns
        -------
        action : str
            a string representing the action the Agent wants to make in the environment.
        '''

        rules_dict = {
            # this is the sequential order of moves in relative roomba space. directions are relative to where roomba is
            # looking, not cardinal environment directions
            "right": "forward",
            "forward": "left",
            "left": "back",
            "back": "error"
        }

        reverse_dict = {
            # this makes the roomba turn around
            # turning around means the roomba's old left is not its right, meaning it will try to stick to a wall that's across from it
            "right": "left",
            "forward": "back",
            "left": "right",
            "back": "forward",
            "suck": "right"
        }

        dirt_percept = self.percepts[-2]
        bump_percept = self.percepts[-1]
        print("-     Agent's POV     -")
        print(f"Dirt Percept: {dirt_percept}")
        print(f"Bump Percept: {bump_percept}")
        print(f"Last Action: {self.action}")

        if dirt_percept == "dirty":  # if dirty
            print("IM SUCKING SUCKING SUCKING SUCKING ")
            self.action = "suck"  # suck
            self.performance += 1  # update your personal score
        else:
            if bump_percept == "bump":  # okay, we tried to move and we hit something, let's take our last action and use it to find a new one
                self.action = rules_dict.get(self.action)
                print("We Bumped - DICTIONARY ACTION")
                print(self.action)
            else:  # we haven't bumped into anything, so try to move right
                print("Not Bumped - NORMAL ACTION")
                # store last successful action

                if self.loop_tracker():  # check for multiple loops
                    # self.action = "right"
                    self.action = reverse_dict.get(self.action)  # turn around and try to attach to a inside/outside wall
                else:
                    self.action = "right"

                print(self.action)

            if self.action == "error":  # we've tried to move everywhere and nothing worked, throw error
                raise AttributeError("Roomba is stuck in a hole, no possible movements")

        self.agent_last_successful = self.cardinal_action
        self.interpret_cardinal_action()
        self.mapping(self.percepts)

        return self.action

class Vacuum_Environment(ABC):
    """
    An abstract class representing a room with nothing (0), clean (1), wall (2), dirty (3)
    ...
    Attributes
    ----------
    world : nested list
        a nested integer list representing the rooms within the vacuum environment as nothing (0), clean (1), wall (2),
        and dirty (3)
    agent_action : str
        the action the agent will do in the environment.
    environment_won : bool
        Keeps track of whether the environment it is currently in is already won.
    score : int
        Keeps track of the number of times the agent has completed the environments' tasks.
    Methods
    -------
    create_world()
        Sets the 'world' class variable representing the different rooms in the environment.
    create_dirt(number_of_dirt)
        Creates number_of_dirt many dirty rooms in random clean rooms in the environment.
    do_kids_create_dirt()
        Randomly creates dirt in a clean room according to the 10% kids creating dirt chance.
    agent_program(agent)
        Makes the object agent's percepts and sets that inside of the agent. Then, it calls agent.rules() to get the
        agent's action and sets that equal to the 'agent_action' class variable.
    change_environment()
        Changes the state of the environment based on the agent_action class variable.
    get_dirt_status()
        Getter for the status of the number of dirty rooms in the room environment.
    __repr__()
        Represents the class when printed as a formatted string of the 'world' class variable with the agent's position
        in the room environment represented by a asterisks (*)
    """

    def __init__(self):
        '''
        Parameters
        ----------
        world : nested list
            a nested integer list representing the rooms within the vacuum environment as nothing (0), clean (1), wall (2),
            and dirty (3)
        agent_action : str
            the action the agent will do in the environment based in cardinal direction
        agent_last_movement : str
            the last succesful action the agent took in the enviornemnt in cardinal direction
        agent_action_relative : str
            the action the agent took in the enviornment in relative orientation
        environment_won : bool
            Keeps track of whether the environment it is currently in is already won.
        score : int
            Keeps track of the number of times the agent has completed the environments' tasks.
        agent_percepts : list
            the complete history of percepts of the agent
        agent_percepts_buffer : 2-item list
            the two most recent percepts of the agent
        agent_position : 2-item list
            the position of the agent in [row, collumn]
        bump : bool
            used to communicate cross function in bump_percept to change_enviornment whether agent has bumped
        '''

        self.world = []
        self.agent_action = ""
        self.agent_last_movement = "right"
        self.agent_action_relative = "right"
        self.environment_won = False
        self.score = 0
        self.agent_percepts = []
        self.agent_percepts_buffer = []
        self.agent_position = [3, 4]
        self.bump = False

    def create_world(self, world_parameter):
        '''
        Sets the 'world' class variable representing the different rooms in the environment.
        The 'world' class variable is an integer list representing the environment and the objects within each room:
        nothing (0), clean (1), wall (2), dirty (3)

        Asserts
        -------
            If yamada is None, assert.
        '''

        # TODO:KOJIRO We can import the world configuration in the main loop and then have a parameter called
        # TODO:KOJIRO world_config that contains the configuration of the world we want to use.
        # TODO:KOJIRO Replace the assert with logging.

        assert world_parameter is not None, "Make sure that you have a variable name with your lastname as the configuration " \
                                   "of your world"
        self.world = read_world(world_parameter)

    def create_dirt(self, number_of_dirt):
        '''
        Creates number_of_dirt many dirty rooms in random clean rooms in the environment.
        Parameters
        ----------
            number_of_dirt : Number of clean rooms to be converted into dirty rooms

        Asserts
        -------
            number_of_dirt cannot be equal to 0
        '''
        assert number_of_dirt != 0, "Cannot make 0 dirt"

        dirt_created = 0 # Number of clean rooms converted into dirty rooms
        while True:
            random_row = randint(0, len(self.world)) # Random row in the world environment
            clean_rooms = self.world[random_row].count(1) # Number of clean rooms in the row of rooms
            if dirt_created == number_of_dirt: # If the desired number of dirty rooms have been created, stop
                break
            elif clean_rooms > 0: # Else if the number of clean rooms in the row is greater than 0. If not, go to
                                  # Another row.
                dirty_room = randint(0, clean_rooms) # The xth clean room in the row is going to become dirty
                clean_room_count = 0 # Number of clean rooms already cycled through
                for i in range(len(self.world)): # Cycle through the desired row
                    if self.world[random_row][i] == 1:
                        if clean_room_count == dirty_room: # If its the desired clean room to be dirty, make it dirty.
                            self.world[random_row][i] = 3
                            continue
                        else:
                            clean_room_count += 1

    def do_kids_create_dirt(self):
        '''
        Randomly creates dirt in a clean room according to the 10% kids creating dirt chance.
        '''
        if randint(0, 10) == 5:
            self.create_dirt(1)

    def agent_percept(self, agent):
        '''
        Runs all the agent percept functions and resets the buffer after checking it.

        Parameters
        ----------
        agent : Object of Agent class
        '''
        self.agent_dirt_sensor(agent)
        self.agent_bump_sensor(agent)
        agent.set_percepts(self.agent_percepts_buffer)
        self.agent_percepts_buffer = []

    def agent_dirt_sensor(self, agent):
        '''
        Adds and sets that inside of the agent. Then, it calls agent.rules() to get the
        agent's action and sets that equal to the 'agent_action' class variable.
        Parameters
        ----------
        agent : Object of Agent class
        '''

        print("-     Dirt Percept      -")
        print(f"Agent Is In: {self.world[self.agent_position[0]][self.agent_position[1]]}")

        if str(self.world[self.agent_position[0]][self.agent_position[1]]) == "DIRTY":
            print("Agent is passed Dirty percept")
            self.agent_percepts.append("dirty")
            self.agent_percepts_buffer.append("dirty")
        else:
            print("Agent is passed Clean percept")
            self.agent_percepts.append("clean")
            self.agent_percepts_buffer.append("clean")

    def agent_bump_sensor(self, agent):
        '''
        Makes the object agent's percepts and sets that inside of the agent. Then, it calls agent.rules() to get the
        agent's action and sets that equal to the 'agent_action' class variable.
        Parameters
        ----------
        agent : Object of Agent class
        '''

        if self.bump:
            self.agent_percepts.append("bump")
            self.agent_percepts_buffer.append("bump")
            self.bump = False
        else:
            self.agent_percepts.append("no bump")
            self.agent_percepts_buffer.append("no bump")

    def change_environment(self):
        '''
        Changes the state of the environment based on the agent_action class variable.
        If the dirty room becomes clean, the 'dirty_room' class variable becomes an empty list since there are no more
        dirty rooms in the environment.
        '''

        print("-     Change Enviornment      -")
        print(f"Agent Is In: {self.world[self.agent_position[0]][self.agent_position[1]]}")

        if self.agent_action == "suck":
            if str(self.world[self.agent_position[0]][self.agent_position[1]]) == "DIRTY":
                print("X  X  X  POGGERS WE JUST CLEANED UP  X  X  X ")
                self.world[self.agent_position[0]][self.agent_position[1]] = clean_tile
                self.score += 1
            else:
                print("ERROR - TRIED TO SUCK IN CLEAN")
                error("TRIED TO SUCK IN CLEAN")
        else:
            # print(self.agent_action)
            movement_vector = string_movement_to_vector.get(self.agent_action)
            print(f"Movement_vector: {movement_vector}")
            print(f"Agent_position: {self.agent_position}")
            test_position = [self.agent_position[0] + movement_vector[0], self.agent_position[1] + movement_vector[1]]
            self.update_agent_position(self.check_bounds(test_position, self.agent_position))

    def update_agent_position(self, position):
        '''
        Changes agent position

        Parameters
        ----------
        position

        Returns
        -------
            Nothing
        '''

        self.agent_position = position

    def __repr__(self):
        '''
        Prints the environment 'world' formatted with nothing as "OUT", clean as "CLEAN", wall as "WALL", and dirty as
        "DIRTY".
        Returns
        -------
        list
            an str list with four states: ["OUT", "CLEAN", "WALL","DIRTY"].
        '''
        world_with_agent = []
        row = []
        for i in range(len(self.world)):
            row = []
            for j in range(len(self.world[i])):
                element = self.world[i][j]
                if i == self.agent_position[0] and j == self.agent_position[1]:
                    row.append(f"Agent + {element}")
                else:
                    row.append(element)
            world_with_agent.append(row)

        # world_with_agent[self.agent_position[0]][self.agent_position[1]] = f"AGENT_POSITION + {agent_is_in}"
        pretty_world = '\n'.join(map(str, world_with_agent))
        return pretty_world

class Normal_Vacuum_Environment(Vacuum_Environment):
    """
    A class representing a vacuum environment for the Model_Agent with nothing (0), clean (1), wall (2), dirty (3)

    Different than normal_vaccuum_enviornment in the way that it records agent movement to figure out where the agent has rotated to,
    similar to how roombas work, depending on whether it bumps or succeeds.

    ...
    Attributes
    ----------
    Methods
    -------
    """

    def agent_update(self, agent):
        '''
        Updates the agent and interprets the agent movement.
        For info on why we're using relative positioning and directions here, see wiki or agent descriptions.

        ----------
        Parameters
            agent : Agent to be updated and taken action from
        ----------
        Variables
            agent_action_relative : Agent's most recent passed back rules
            agent_last_movement : Agent's most recent successful action (action which didn't result in bump)
            agent_action : Resultant Decrypted Action
        '''
        self.agent_action_relative = agent.rules()
        if self.agent_action_relative != "suck":
            print("_____ Interpreting Agent Action _____")
            print(f"Relative Action: {self.agent_action_relative}")
            print(f"Interpreted Bearing Action: {self.agent_last_movement}")
            self.agent_action = str(movement_decrypt[self.agent_last_movement][self.agent_action_relative])
        else:
            self.agent_action = self.agent_action_relative
        print(f"Resultant Action: {self.agent_action}")

    def check_bounds(self, test_position, old_position):
        '''
        Checks whether the Agent movement will result in a Bump or result in movement.

        ----------
        Parameters
            test_position : the proposed position after the agents movement has been applied to current position
            old_position : the current agent position
        ----------
        Variables
            agent_last_movement : Agent's most recent successful action (action which didn't result in bump)
        ----------
        Returns
            position : [y coordinate, x coordinate]
        '''

        print(f"Test Position: {test_position}")
        if 0 <= test_position[0] < 6 and 0 <= test_position[1] < 7:
            if str(self.world[test_position[0]][test_position[1]]) != "WALL" and str(self.world[test_position[0]][test_position[1]]) != "OUT":
                self.agent_last_movement = self.agent_action
                print(f"Success: Test Position Valid, Returning : {test_position}")
                return test_position
            else:
                print(f"Failure: Bumped Into WALL, Returning : {old_position}")
                self.bump = True
                return old_position
        else:
            print(f"Failure: Bumped Into OUT OF BOUNDS, Returning : {old_position}")
            self.bump = True
            return old_position

class Simple_Vacuum_Environment(Vacuum_Environment):
    """
    A class representing a vacuum environment for the Reflex_Agent with nothing (0), clean (1), wall (2), dirty (3)

    Different than normal_vaccuum_enviornment in the way that it
    records agent movement to figure out where the agent has rotated to regardless of it's success

    Normal vaccuum enviiornment only changes agent headiing if it doesn't bump into anything

    ...
    Attributes
    ----------
    Methods
    -------
    """

    def agent_update(self, agent):
        '''
        Updates the agent and interprets the agent movement.
        This enviornment has one key difference, we ALWAYS make agent heading to last action regardless of success
        For info on why we're using relative positioning and directions here, see wiki or agent descriptions.

        ----------
        Parameters
            agent : Agent to be updated and taken action from
        ----------
        Variables
            agent_action_relative : Agent's most recent passed back rules
            agent_last_movement : Agent's most recent action - UNLIKE THE NORMAL ENVIORNMENT
            agent_action : Resultant Decrypted Action
        '''
        self.agent_action_relative = agent.rules()
        if self.agent_action_relative != "suck":
            self.agent_action = movement_decrypt.get(self.agent_last_movement).get(self.agent_action_relative)
            self.agent_last_movement = self.agent_action
        else:
            self.agent_action = self.agent_action_relative

    def check_bounds(self, test_position, old_position):
        '''
        Checks whether the Agent movement will result in a Bump or result in movement.

        ----------
        Parameters
            test_position : the proposed position after the agents movement has been applied to current position
            old_position : the current agent position
        ----------
        Variables
            agent_last_movement : Agent's most recent successful action (action which didn't result in bump)
        ----------
        Returns
            position : [y coordinate, x coordinate]
        '''

        if self.world[test_position[0]][test_position[1]] == 3:
            self.bump = True
            return old_position
        else:
            return test_position

if __name__ == '__main__':
    '''
    The main loop of the program.
    Variables
    ----------
    total_score : into
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
    out_tile = Tile.out()
    clean_tile = Tile.clean()
    wall_tile = Tile.wall()
    dirty_tile = Tile.dirty()
    total_score = 0
    step_max = 1000
    steps = 0
    run = True
    vacuum_world = Normal_Vacuum_Environment()
    vacuum_world.create_world(yamada)
    print(f"Initial State: \n{vacuum_world}")
    roomba = Model_Agent()
    while run:
        if steps == step_max:
            run = False
        print("-------------------------")
        print(f"Step # {steps}")
        vacuum_world.agent_percept(roomba)
        vacuum_world.agent_update(roomba)
        vacuum_world.change_environment()
        # vacuum_world.do_kids_create_dirt()
        print("-    Other Debug Info     -")
        print(f"World State: {vacuum_world}")
        print(f"Agent Percept: {roomba.percepts}")
        print(f"Action: {roomba.action}")
        print(f"Last Passed Action: {vacuum_world.agent_last_movement}")
        print(f"Agent Position: {vacuum_world.agent_position}")
        print(f"Latest Roomba Performance: {roomba.performance}")
        print(f"Latest World Performance: {vacuum_world.score}")
        steps += 1

    total_score += vacuum_world.score
    if total_score > 0:
        print(f"\nThe roomba has completed the task(s) in the environment(s) {total_score} times.")
    else:
        print("\nThe roomba has not completed the task(s) in the environment.")

    print("FIX REPRESENT DUMBASS")
    print("Make Random Location")
    print("Make dirt kids")
