from random import randint
import logging


def setup_logging(level=logging.DEBUG):
    logging.basicConfig(level=level, format='%(asctime)s{%(levelname)s} %(message)s', datefmt='%H:%M:%S')

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
    right: {"right": "down", "left": "up", "forward": "right", "back": "left"},
    left: {"right": "up", "left": "down", "forward": "left", "back": "right"},
    up: {"right": "right", "left": "left", "forward": "up", "back": "down"},
    down: {"right": "left", "left": "right", "forward": "down", "back": "up"}
}

# this converts cardinal movements to vectors
string_movement_to_vector = {
    right: [0,1],
    left: [0,-1],
    up: [-1,0],
    down: [1,0],
    suck: [-99,-99] # should throw error
}



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
        self.action = "right"

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

        dirt_percept = self.percepts[-1][-1]
        bump_percept = self.percepts[-1][-2]

        if dirt_percept == "dirty":  # if dirty
            self.action = "suck" # suck
            self.performance += 1 # update your personal score
        else:
            if bump_percept == "bump":  # okay, we tried to move and we hit something, let's take our last action and use it to find a new one
                self.action = rules_dict.get(self.action)
            else: # we haven't bumped into anything, so try to move right
                if randint(0, 100) < 5: # random case to help us get to harder-to-reach areas
                    self.action = reverse_dict.get(self.action) # turn around and try to attach to a inside/outside wall
                else:
                    self.action = "right"

            if self.action == "error":  # we've tried to move everywhere and nothing worked, throw error
                raise AttributeError("Roomba is stuck in a hole, no possible movements")

        return self.action

class ModelAgent:
    '''
    A class that represents an Agent in the Environment.

    ...

    Attributes
    ----------
    percepts : list
        tells whether the agent has bumped into a wall, whether the ground/wall is clean

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
            virtual_ruleset(self, self.action, bump_percept)

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
            if "theres virtual blocks" = "test" # oh wait looks like we locked ourself in, let's delete those blocks
                # delete virtual blocks
                # continue and attach
                virtual_ruleset("right", "no bump")
                return
            else: # holdup that wasn't us, the map creator messed up, time to raise an error
                raise AttributeError("Roomba is stuck in a hole")

        if virtual_bump_check(proposed_action): # let's run virtual bump check to see if that's a virtual block
            virtual_ruleset(proposed_action, "bump") # if it is, regenerate the rules and dupe it into thinking it bumped into a real block and it didn't work
        else:
            self.action = proposed_action # this won't hit a virtual block, time to see if it'll hit a real one

    def virtual_bump_check(self, proposed_action):
        return true
    
    def mapping(self, agent_percepts):
        '''agent tries to construct a map of the world based on past experience'''
        world=[[0]]
        agent_col=0                                                           # variable keeps track of agent's collumn (relative to starting location)
        agent_row=0                                                           # keeps track of agent's row
        if self.action=="right" and agent_percepts!= "bump":                  # agent has successfully moved right
            agent_col+=1
            if len(world[agent_row])>=agent_col:                              # checks if this area of the row has already been explored
                world[agent_row][agent_col]=0
            if len(world[agent_row])<agent_col-1:                             # makes sure agent has only been moved by one square (I don't know what would cause a skip but I want to make sure we know if it happens)
                AttributeError("Mapping error: agent has skipped a square")
            else:                                                             # agent has not already mapped this square
                world[agent_row].insert(agent_col,0)                          # zero is added at agent's new location
        if self.action=="left" and agent_percepts!= "bump":
            if agent_col>0:                                                   # checks if agent is on the edge of its mapped area
                agent_col-=1
                world[agent_row][agent_col]=0                                 # if not, adds zero at agent's new location
            else:
                world[agent_row].insert(agent_col,0)                          # adds zero at the left edge of the mapped area
        if self.action=="up" and agent_percepts!= "bump":
            if agent_row==0:
                templist=[-]*(agent_col-((agent_col>0)*1))                    # makes a list of filler items to make sure that collumns are aligned, only subtracts 1 if the column number isn't 0
                world.insert(0,templist)                                      # adds filler list to the row above agent
                world[0].append(0)                                            # adds a zero at the agent's new position
            else:
                agent_row-=1
                if len(world[agent_row])>len(world[agent_row+1]):             # checks if new row has more filled in slots than old row (has it been explored more)
                    world[agent_row].insert(agent_col,0)                      # makes sure agent's new position is marked as empty
                else:
                    row_dif=(len(world[agent_row+1]-len(world[agent_row])))-1 # prepares filler list to make up for difference in row lengths (due to difference in exploration)
                    templist=[-]*row_dif                                      # filler list
                    world[agent_row].extend(templist)                         # inserts filler list to agent's new row
                    world[agent_row].insert(agent_col,0)                      # adds 0 at agent's new position
        if self.action=="down" and agent_percepts!="bump":
            agent_row+=1
            if world[agent_row-1]==world[-1]:                                 # checks if previous row was the bottom row
                templist=[-]*(agent_col-((agent_col>0)*1))
                world.append(templist)
                world[agent_row].insert(agent_col,0)
            else:
                if len(world[agent_row])>len(world[agent_row-1]):             # checks if new row has been filled in more than old row
                    world[agent_row].insert(agent_col,0)                      # makes sure agent's position is marked as empty
                else:
                    row_dif=len(world[agent_row])-len(world[agent_row-1])-1   # prepares filler list to make up for difference in row lengths
                    templist=[-]*row_dif                                      # filler list
                    world[agent_row].extend(templist)                         # insterts filler list into agent's new row
                    world[agent_row].insert(agent_col,0)                      # adds zero at agent's current location

class Vacuum_Environment:
    """
    A class representing a room with nothing (0), floors (1), walls (2), dirty_floor (3), dirty_walls (4)

    ...

    Attributes
    ----------
    world : list
        an integer list representing the room and the objects within the room: nothing (0), floors (1), walls (2),
        dirty_floor (3), dirty_walls (4)
    agent_action : str
        the action the agent will do in the environment.
    environment_won : bool
        Keeps track of whether the environment it is currently in is already won.
    score : int
        Keeps track of the number of times the agent has completed the environments' tasks.

    Methods
    -------
    create_world()
        Sets the 'world' class variable representing the room and the objects within it.

    create_dirt(number_of_dirt)
        Spawns in "number_of_dirt" many dirt into the room environment.

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
        world : list
            an integer list representing the room and the objects within the room: nothing (0), floors (1), walls (2),
            dirty_floor (3), dirty_walls (4)
        agent_action : str
            the action the agent will do in the environment.
        environment_won : bool
            Keeps track of whether the environment it is currently in is already won.
        score : int
            Keeps track of the number of times the agent has completed the environments' tasks.
        '''

        self.world = [[]]
        self.agent_action = ""
        self.agent_last_movement = "right"
        self.agent_action_relative = ""
        self.environment_won = False
        self.score = 0
        self.agent_percepts = []
        self.agent_percepts_buffer = []

    def create_world(self, world_config):
        '''
        Sets the 'world' class variable representing the rooms of the environment and agent inside of it.
        The 'world' class variable represents the location of the agent and the room that it is in.

        Parameters
        ----------
        world_config : list
            an integer list representing the room and the objects within the room: nothing (0), floors (1), walls (2),
            dirty_floor (3), dirty_walls (4)

        Raises
        ------
        AttributeError
            If there is already a pre-existing 'world', this will prevent overriding it with a new 'world'.
        '''

        if self.world == []:
            if world_config != None:
                raise NotImplementedError("Other world configurations haven't been created yet!")
            else:
                self.world = world_config
        else:
            raise AttributeError("Can't create new world. Pre-existing world exists!")

    def do_kids_create_dirt(self):
        '''
        Randomly creates dirt in empty spaces accoding to the 10% kids creating dirt chance.

        '''

        for "all empty spaces"
            if randint(0, 100) < 11
                "make that space dirty"

    def agent_percept(self, agent):
        agent_dirt_sensor(agent)
        agent_bump_sensor(agent)
        agent.set_percepts(self.agent_percepts_buffer)

    def agent_dirt_sensor(self, agent):
        '''
        Adds and sets that inside of the agent. Then, it calls agent.rules() to get the
        agent's action and sets that equal to the 'agent_action' class variable.

        Parameters
        ----------
        agent : Object of Agent class
        '''

        if "we're in a clean space":
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

    def agent_update(self, agent):
        self.agent_action_relative = agent.rules()
        if self.agent_action_relative != "suck":
            self.agent_action = movement_decrypt.get(self.agent_last_movement).get(self.agent_action_relative)
        else:
            self.agent_action = self.agent_action_relative

    def change_environment(self):
        '''
        Changes the state of the environment based on the agent_action class variable.
        If the dirty room becomes clean, the 'dirty_room' class variable becomes an empty list since there are no more
        dirty rooms in the environment.
        '''

        if self.agent_action == "suck" and "we're in a dirty space":
            "make dirty room clean"
            self.score += 1
        else:
            movement_vector = string_movement_to_vector.get(self.agent_action)
            test_position = "take position and add movement_vector"
            agent_position = check_bounds(test_position, agent_position)

    def check_bounds(self, test_position, old_position):
        if "test_postion is out of bounds or a wall is there":
            self.bump = True
            return old_position
        else:
            return test_position
            self.agent_last_movement = self.agent_action

    def update_agent_position(self, position):
        "make agent position" = position

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

class Simplest_Agent:
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

        How our rules work is such:
        We're always sticking to the right, so the first thing we ALWAYS do is try to move right.
        If we tried to move right last action, and we got back a bump in our percept, let's try to move Forward, etc.
        Right -> Forward -> Left -> Back

        The
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

class Simplest_Vacuum_Environment:
    """
    A class representing a room with nothing (0), clean (1), wall (2), dirty (3)

    ...

    Attributes
    ----------
    world : list
        an integer list representing the room and the objects within the room: nothing (0), clean (1), wall (2),
        dirty (3)
    agent_action : str
        the action the agent will do in the environment.
    environment_won : bool
        Keeps track of whether the environment it is currently in is already won.
    score : int
        Keeps track of the number of times the agent has completed the environments' tasks.

    Methods
    -------
    create_world()
        Sets the 'world' class variable representing the room and the objects within it.

    create_dirt(number_of_dirt)
        Spawns in "number_of_dirt" many dirt into the room environment.

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
        world : list
            an integer list representing the room and the objects within the room: nothing (0), clean (1), wall (2),
            dirty (3)
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
        self.agent_action_relative = ""
        self.environment_won = False
        self.score = 0
        self.agent_percepts = []
        self.agent_percepts_buffer = []
        self.agent_position = [0,0]

    def create_world(self):
        '''
        Sets the 'world' class variable representing the different rooms in the environment.
        The 'world' class variable is an integer list representing the environment and the objects within each room:
        nothing (0), clean (1), wall (2), dirty (3)

        Asserts
        -------

        '''

        # TODO:KOJIRO We can import the world configuration in the main loop and then have a parameter called
        # TODO:KOJIRO world_config that contains the configuration of the world we want to use.
        # TODO:KOJIRO Replace the assert with logging.

        from hw4_util import read_world
        from yamada_world import yamada

        assert yamada is not None, "Make sure that you have a variable name with your lastname as the configuration " \
                                   "of your world"
        self.world = read_world(yamada)

    def do_kids_create_dirt(self):
        '''
        Randomly creates dirt in a clean room according to the 10% kids creating dirt chance.
        '''
        if randint(0,10) == 5:
            for list, row in enumerate(self.world):
                for element, column in enumerate(list):  # Cycles through the elements in the world matrix.
                    if element == 1:  # Checks to see whether the selected element is representing a clean room.
                        if randint(0, 10) == 5: # 5 is an arbitrary number between 0 to 9. 10% chance of being true.
                            self.world[row][column] = 3  # makes the selected clean room into a dirty room.


    def agent_percept(self, agent):
        agent_dirt_sensor(agent)
        agent_bump_sensor(agent)
        agent.set_percepts(self.agent_percepts_buffer)

    def agent_dirt_sensor(self, agent):
        '''
        Adds and sets that inside of the agent. Then, it calls agent.rules() to get the
        agent's action and sets that equal to the 'agent_action' class variable.

        Parameters
        ----------
        agent : Object of Agent class
        '''

        if self.world[agent_position[0]][agent_position[1]] == 3:
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

    def agent_update(self, agent):
        self.agent_action_relative = agent.rules()
        if self.agent_action_relative != "suck":
            self.agent_action = movement_decrypt.get(self.agent_last_movement).get(self.agent_action_relative)
            self.agent_last_movement = self.agent_action
        else:
            self.agent_action = self.agent_action_relative

    def change_environment(self):
        '''
        Changes the state of the environment based on the agent_action class variable.
        If the dirty room becomes clean, the 'dirty_room' class variable becomes an empty list since there are no more
        dirty rooms in the environment.
        '''

        if self.agent_action == "suck" and self.world[agent_position[0]][agent_position[1]] == 3:
            self.world[agent_position[0]][agent_position[1]] = 1
            self.score += 1
        else:
            movement_vector = string_movement_to_vector.get(self.agent_action)
            test_position = [agent_position[0] + movement_vector[0], agent_position[1] + movement_vector[1]]
            self.agent_position = check_bounds(test_position, agent_position)

    def check_bounds(self, test_position, old_position):
        if self.world[test_position[0]][test_position[1]] == 3:
            self.bump = True
            return old_position
        else:
            return test_position

    def update_agent_position(self, position):
        self.agent_position = position

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
    step_max = 1000
    steps = 0
    run = True
    vacuum_world = Vacuum_Environment()
    vacuum_world.create_world()
    vacuum_world.create_dirt()
    print(f"Initial State: {vacuum_world}")
    roomba = Agent()
    while run:
        if steps == step_max:
            run = False
        print(f"Step # {steps}")
        vacuum_world.agent_percept(roomba)
        vacuum_world.agent_update(roomba)
        vacuum_world.change_environment()
        print(f"World State: {vacuum_world}")
        print(f"Agent Percept: {roomba.percepts}")
        print(f"Action: {roomba.action}")
        print(f"Latest Performance: {roomba.performance}")
        steps += 1

    total_score += vacuum_world.score
    if total_score > 0:
        print(f"\nThe roomba has completed the task(s) in the environment(s) {total_score} times.")
    else:
        print("\nThe roomba has not completed the task(s) in the environment.")