
class Tile:
    """ stores the 4 types of tiles in the world"""

    OUT = 0
    CLEAN = 1
    WALL = 2
    DIRTY = 3

    def __repr__(self):
        if self.value == Tile.OUT:
            return "OUT"
        elif self.value == Tile.CLEAN:
            return "CLEAN"
        elif self.value == Tile.WALL:
            return "WALL"
        else:
            return "DIRTY"
    
    def __init__(self):
        pass

    @classmethod
    def wall(cls):
        t = Tile()
        t.value = Tile.WALL
        return t

    @classmethod
    def out(cls):
        t = Tile()
        t.value = Tile.OUT
        return t

    @classmethod
    def clean(cls):
        t = Tile()
        t.value = Tile.CLEAN
        return t

    @classmethod
    def dirty(cls):
        t = Tile()
        t.value = Tile.DIRTY
        return t

            


def read_world(world_definition, rows=6, cols=7):
    """parse a world_definition file with rows*cols space delimited values"""
    out = Tile.out()
    clean = Tile.clean()
    wall = Tile.wall()
    dirty = Tile.dirty()

    #symbol dictionary for world file
    legend = { '-': out, '0': clean, '1': wall, '2': dirty }

    # split on whitespace
    input = world_definition.split(' ')
    # remove any blank input
    input = [v for v in input if len(v) > 0]

    assert len(input) == rows * cols, "The dimensions of your world"\
        " are wrong got: {} expected: {}".format(rows*cols, len(input))

    records = [input[ (i*cols):(i*cols + cols) ] for i in range(6)]
    world = []
    for r in records:
        data = []
        for v in r:
            # some values may contain more than 1 value comma delimited...
            if "," in v:
                _v = v.split(",")
                nested_data = []
                for _v_ in _v:
                    nested_data.append( legend[_v_] )
                data.append( nested_data )
            # ... or it is just a single value
            else:
                data.append( legend[v] )
        world.append(data)

    return world

# def world_to_string(world_matrix, rows=6, cols=7):
#     # states = ["OUT", "CLEAN", "WALL","DIRTY"]
#     states = [Tile.out(), Tile.clean(), Tile.wall(), Tile.dirty()]

#     # use a nested list comprehension to iterate the 2D list
#     # the value is just an index into a list of strings, states.
#     return [ [ states[val] for val in row ] for row in world_matrix ]



if __name__ == '__main__':
    from yamada_world import yamada

    world = read_world(yamada)

    print(world)