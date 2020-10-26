def get_direction(direction):
    if direction == 'A':
        return Variable.ACROSS
    elif direction == 'D':
        return Variable.DOWN


class Variable:
    ACROSS = "across"
    DOWN = "down"

    """Create a new variable with starting point, direction, and length."""
    def __init__(self, number, direction, length, i, j):
        self.number = number
        self.direction = get_direction(direction)
        self.length = length
        self.i = i
        self.j = j
        self.cells = []
        for k in range(self.length):
            self.cells.append(
                (self.i + (k if self.direction == Variable.DOWN else 0),
                 self.j + (k if self.direction == Variable.ACROSS else 0))
            )

    def __hash__(self):
        return hash((self.number, self.direction, self.length, self.i, self.j))

    def __eq__(self, other):
        return (
                (self.number == other.number) and
                (self.direction == other.direction) and
                (self.length == other.length) and
                (self.i == other.i) and
                (self.j == other.j)
        )

    def __str__(self):
        return f"({self.i}, {self.j}) {self.number} {self.direction} : {self.length}"

    def __repr__(self):
        direction = repr(self.direction)
        return f"Variable({self.i}, {self.j}, {self.number}, {direction}, {self.length})"


class Crossword:

    def __init__(self, structure_file, clues_file):

        # Determine structure of crossword
        with open(structure_file) as f:
            contents = f.read().splitlines()
            self.height = len(contents)
            self.width = max(len(line) for line in contents)

            self.structure = []
            for i in range(self.height):
                row = []
                for j in range(self.width):
                    if j >= len(contents[i]):
                        row.append(False)
                    elif contents[i][j] == "_":
                        row.append(True)
                    else:
                        row.append(False)
                self.structure.append(row)

        self.variables = set()
        with open(clues_file) as f:
            contents = f.read().splitlines()
            for line in contents:
                values = line.split(',')
                self.variables.add(Variable(
                    number=int(values[0]),
                    direction=values[1],
                    length=int(values[2]),
                    i=int(values[3]),
                    j=int(values[4])))

        # Compute overlaps for each word
        # For any pair of variables v1, v2, their overlap is either:
        #    None, if the two variables do not overlap; or
        #    (i, j), where v1's ith character overlaps v2's jth character
        self.overlaps = dict()
        for v1 in self.variables:
            for v2 in self.variables:
                if v1 == v2:
                    continue
                cells1 = v1.cells
                cells2 = v2.cells
                intersection = set(cells1).intersection(cells2)
                if not intersection:
                    self.overlaps[v1, v2] = None
                else:
                    intersection = intersection.pop()
                    self.overlaps[v1, v2] = (
                        cells1.index(intersection),
                        cells2.index(intersection)
                    )

    def neighbors(self, var):
        """Given a variable, return set of overlapping variables."""
        return set(
            v for v in self.variables
            if v != var and self.overlaps[v, var]
        )
