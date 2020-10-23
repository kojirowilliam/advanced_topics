from abc import ABC, abstractmethod
from random import randint
import logging

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
# the second dictionary defines what this means for the relative actions of the agent, for example, if you're facing down and take a right, that's going left in world directions
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
        self.action = "right"
        self.world = [[0]]
        self.agent_col = 0  # variable keeps track of agent's collumn (relative to starting location)
        self.agent_row = 0  # keeps track of agent's row

    def set_percepts(self, agent_percepts):
        '''
        Sets the agent's perception of the environment.
        Parameters
        ----------
        percepts : list
            A list of strings and/or Nones that represents the environment from the Agent's perceptions
        '''

        self.percepts = agent_percepts

    @abstractmethod
    def rules(self):
        pass

class Reflex_Agent(Agent):
    '''
    A class that represents a Reflex Agent in the Environment.
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
        return "Reflex_Agent"

    def rules(self):
        '''
        Returns an action depending on the agent's perceptions of the environment.
        How our rules work is such:
        We're always sticking to the right, so the first thing we ALWAYS do is try to move right.
        If we tried to move right last action, and we got back a bump in our percept, let's try to move Forward, etc.
        Right -> Forward -> Left -> Back
        All the agent knows how to do is see if it bumped, then it chooses a new movement, or it isn't bumped, so it moves right
        Remember, these are relative movements, the roomba doesn't know which way is up or down.
        The enviornment knows which way the Roomba is pointing however. The way the roomba is pointing and it's action is decryrpted by the enviornment.
        This allows us to stick to the right, even when we're facing left, down, up, or right. We always move to the relative right.
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
            "back": "forward"
        }

        dirt_percept = self.percepts[-2]
        bump_percept = self.percepts[-1]
        print(f"Dirt Percept: {dirt_percept}")
        print(f"Bump Percept: {bump_percept}")

        if dirt_percept == "dirty":  # if dirty
            print("SUCKING SUCKING SUCKING SUCKING ")
            self.action = "suck" # suck
            self.performance += 1 # update your personal score
        else:
            if bump_percept == "bump":  # okay, we tried to move and we hit something, let's take our last action and use it to find a new one
                self.action = rules_dict.get(self.action)
                print("BUMP - DICTIONARY ACTION")
                print(self.action)
            else: # we haven't bumped into anything, so try to move right
                print("NO BUMP - NORMAL ACTION")
                if randint(0, 100) < 5: # random case to help us get to harder-to-reach areas
                    self.action = reverse_dict.get(self.action) # turn around and try to attach to a inside/outside wall
                else:
                    self.action = "right"

                print(self.action)

            if self.action == "error":  # we've tried to move everywhere and nothing worked, throw error
                raise AttributeError("Roomba is stuck in a hole, no possible movements")

        return self.action

class Simple_Agent(Agent):
    '''
    A class that represents a Reflex Agent in the Environment.
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

class Model_Based_Agent:
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

    def agent_type(self):
        return "Model_Agent"

    def rules(self):
        '''
        Returns an action depending on the agent's perceptions of the environment.
        How our rules work is such:
        We're always sticking to the right, so the first thing we ALWAYS do is try to move right.
        If we tried to move right last action, and we got back a bump in our percept, let's try to move Forward, etc.
        Right -> Forward -> Left -> Back
        But this agent is MUCH SMARTER than the last one because we now can maintain state of the world.
        What we're doing now is trying to spiral around the world until we reach the inside.
        In order to spiral inwwards, we need to pretend like there's blocks in certain spaces : "Virtual Walls"
        These Virtual Walls should impede our movement, but they don't exist in the enviornment, the enviornment has no idea about them
        What we're doing here is doing our normal movement code, then checking if that movement will cause a bump into our Virtual Walls.
        If that movement will make us go into a virtual wall, we send it back to regenerate, making the rules think we just bumped into something and it's the next step, but it isn't
        This creates the recursive nature of our virtual code.
        Remember, these are relative movements, the roomba doesn't know which way is up or down.
        The enviornment knows which way the Roomba is pointing however. The way the roomba is pointing and it's action is decryrpted by the enviornment.
        This allows us to stick to the right, even when we're facing left, down, up, or right. We always move to the relative right.
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
        else:
            # if we haven't tried to move yet, let's move right
            self.virtual_ruleset(self, self.action, bump_percept)

        return self.action

    def virtual_ruleset(self, prev_action, bump_percept):
        rules_dict = {
            # this is the sequential order of moves in relative roomba space. directions are relative to where roomba is
            # looking, not cardinal environment directions
            "right": "forward",
            "forward": "left",
            "left": "back",
            "back": "error"
        }

        if bump_percept == "bump":  # okay, we tried to move and we hit something, let's take our last action and use it to find a new one
            proposed_action = rules_dict.get(prev_action)
        else:
            proposed_action = "right"

        if proposed_action == "error":
            # we've tried everything and we're stuck, make sure we didn't just put ourself into a hole with virtual blocks
            if self.virtual_box_check():  # oh wait looks like we locked ourself in, let's delete those blocks
                # delete virtual blocks
                # continue and attach
                self.virtual_ruleset("right", "no bump")
                return
            else:  # holdup that wasn't us, the map creator messed up, time to raise an error
                raise AttributeError("Roomba is stuck in a hole")
        else:
            if self.virtual_bump_check(proposed_action):  # let's run virtual bump check to see if that's a virtual block
                self.virtual_ruleset(proposed_action, "bump")  # if it is, regenerate the rules and dupe it into thinking it bumped into a real block and it didn't work
            else:
                self.action = proposed_action  # this won't hit a virtual block, time to see if it'll hit a real one

    def virtual_box_check(self):
        return True

    def virtual_bump_check(proposed_action):
        return True

    def prepmap(x, y):
        row = ['-'] * ((2 * x) - 1)
        self.world = [row] * ((2 * y) - 1)
        self.agent_col = x - 1
        self.agent_row = y - 1
        return (self.world)

    def mapping(self, agent_percepts):
        '''agent tries to construct a map of the world based on past experience'''
        if self.action == "right":  # agent moves right
            if agent_percepts != "bump":  # agent has not ran into a wall
                self.agent_col += 1  # collumn variable changed
                self.world[self.agent_row][self.agent_col] = 1  # agent's new square marked as empty
            if agent_percepts == "bump":  # agent has ran into wall
                self.world[self.agent_row][self.agent_col + 1] = 2  # square to the right of the agent marked as wall
        if self.action == "left":  # agent moves left
            if agent_percepts != "bump":  # agent has not ran into wall
                self.agent_col -= 1  # collumn variable changed appropriately
                self.world[self.agent_row][self.agent_col] = 1  # agent's new position marked as empty
            if agent_percepts == "bump":  # agent has hit a wall
                self.world[self.agent_row][self.agent_col - 1] = 2  # square to the left of agent marked as wall
        if self.action == "up":  # agent moves up
            if agent_percepts != "bump":  # agent has not hit a wall
                self.agent_row -= 1  # row variable decreased
                self.world[self.agent_row][self.agent_col] = 1  # agent's new position marked as empty
            if agent_percepts == "bump":  # agent has encountered a wall
                self.world[self.agent_row - 1][self.agent_col] = 2  # square directly above agent marked as wall
        if self.action == "down":  # agent moves down
            if agent_percepts != "bump":  # agent does not hit wall
                self.agent_row += 1  # row variable changed accordingly
                self.world[self.agent_row][self.agent_col] = 1  # agent's new position marked as empty
            if agent_percepts == "bump":  # agent has encountered wall
                self.world[self.agent_row + 1][self.agent_col] = 2  # square directly below agent marked as wall

    def get_pos_value(x, y):  # returns the value of a position on the map
        return self.world[x][y]

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
            the action the agent will do in the environment.
        environment_won : bool
            Keeps track of whether the environment it is currently in is already won.
        score : int
            Keeps track of the number of times the agent has completed the environments' tasks.
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

    def create_world(self):
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

        from hw4_util import read_world
        from yamada_world import yamada

        assert yamada is not None, "Make sure that you have a variable name with your lastname as the configuration " \
                                   "of your world"
        self.world = read_world(yamada)

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
        assert number_of_dirt == 0, "Cannot make 0 dirt"

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
        if randint(0,10) == 5:
            self.create_dirt(1)

    def agent_percept(self, agent):
        self.agent_dirt_sensor(agent)
        self.agent_bump_sensor(agent)
        agent.set_percepts(self.agent_percepts_buffer)

    def agent_dirt_sensor(self, agent):
        '''
        Adds and sets that inside of the agent. Then, it calls agent.rules() to get the
        agent's action and sets that equal to the 'agent_action' class variable.
        Parameters
        ----------
        agent : Object of Agent class
        '''

        if self.world[self.agent_position[0]][self.agent_position[1]] == "DIRTY":
            self.agent_percepts_buffer.append("clean")
        else:
            self.agent_percepts_buffer.append("dirty")

    def agent_bump_sensor(self, agent):
        '''
        Makes the object agent's percepts and sets that inside of the agent. Then, it calls agent.rules() to get the
        agent's action and sets that equal to the 'agent_action' class variable.
        Parameters
        ----------
        agent : Object of Agent class
        '''

        if self.bump:
            self.agent_percepts_buffer.append("bump")
            self.bump = False
        else:
            self.agent_percepts_buffer.append("no bump")

    def change_environment(self):
        '''
        Changes the state of the environment based on the agent_action class variable.
        If the dirty room becomes clean, the 'dirty_room' class variable becomes an empty list since there are no more
        dirty rooms in the environment.
        '''

        print("-     Change Enviornment      -")
        print(f"Action: {self.agent_action}")
        print(f"Agent Is In: {self.world[self.agent_position[0]][self.agent_position[1]]}")

        if self.agent_action == "suck":
            if self.world[self.agent_position[0]][self.agent_position[1]] == "DIRTY":
                self.world[self.agent_position[0]][self.agent_position[1]] = 1
                self.score += 1
            else:
                print("Tried to suck in clean")
                error("TRIED TO SUCK IN CLEAN")
        else:
            # print(self.agent_action)
            movement_vector = string_movement_to_vector.get(self.agent_action)
            print(f"Movement_vector: {movement_vector}")
            print(f"Agent_position: {self.agent_position}")
            test_position = [self.agent_position[0] + movement_vector[0], self.agent_position[1] + movement_vector[1]]
            self.update_agent_position(self.check_bounds(test_position, self.agent_position))

    def update_agent_position(self, position):
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
        return "Represent is currently broken"

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
        self.agent_action_relative = agent.rules()
        if self.agent_action_relative != "suck":
            self.agent_action = movement_decrypt[self.agent_last_movement][self.agent_action_relative]
        else:
            self.agent_action = self.agent_action_relative

    def check_bounds(self, test_position, old_position):
        print(f"Test Position: {test_position}")
        if 0 <= test_position[0] < 6 and 0 <= test_position[1] < 7:
            if self.world[test_position[0]][test_position[1]] != "WALL" and self.world[test_position[0]][test_position[1]] != "OUT":
                self.agent_last_movement = self.agent_action
                return test_position
            else:
                print("XXX --- Bumped into a wall --- XXX")
                self.bump = True
                # info("Bump Wall")
                return old_position
        else:
            print("XXX --- Out of Bounds --- XXX")
            self.bump = True
            # warn("Bump Out of Bounds")
            return old_position

class Simple_Vacuum_Environment(Vacuum_Environment):
    """
    A class representing a vacuum environment for the Reflex_Agent with nothing (0), clean (1), wall (2), dirty (3)

    Different than normal_vaccuum_enviornment in the way that it records agent movement to figure out where the agent has rotated to regardless of it's success

    ...
    Attributes
    ----------
    Methods
    -------
    """

    def agent_update(self, agent):
        self.agent_action_relative = agent.rules()
        if self.agent_action_relative != "suck":
            self.agent_action = movement_decrypt.get(self.agent_last_movement).get(self.agent_action_relative)
            self.agent_last_movement = self.agent_action
        else:
            self.agent_action = self.agent_action_relative

    def check_bounds(self, test_position, old_position):
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

    total_score = 0
    step_max = 200
    steps = 0
    run = True
    vacuum_world = Normal_Vacuum_Environment()
    vacuum_world.create_world()
    print(f"Initial State: {vacuum_world}")
    roomba = Reflex_Agent()
    while run:
        if steps == step_max:
            run = False
        print("-------------------------")
        print(f"Step # {steps}")
        vacuum_world.agent_percept(roomba)
        vacuum_world.agent_update(roomba)
        vacuum_world.change_environment()
        print("-    Other Debug Info     -")
        print(f"World State: {vacuum_world}")
        print(f"Agent Percept: {roomba.percepts}")
        print(f"Action: {roomba.action}")
        print(f"Last Passed Action: {vacuum_world.agent_last_movement}")
        print(f"Agent Position: {vacuum_world.agent_position}")
        print(f"Latest Performance: {roomba.performance}")
        steps += 1

    total_score += vacuum_world.score
    if total_score > 0:
        print(f"\nThe roomba has completed the task(s) in the environment(s) {total_score} times.")
    else:
        print("\nThe roomba has not completed the task(s) in the environment.")
