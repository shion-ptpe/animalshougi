class Piece:
    @classmethod
    def deserialize(_, char: str, captured=False):
        if not (type(char) is str):
            raise TypeError
        elif len(char) > 1:
            raise ValueError("length of input must be 1")
        is_sente: bool = (char == char.upper())
        match char.upper():
            case "C":
                return Chick(0, captured) if is_sente else Chick(1, captured)
            case "L":
                return Lion(0, captured) if is_sente else Lion(1, captured)
            case "G":
                return Giraffe(0, captured) if is_sente else Giraffe(1, captured)
            case "E":
                return Elephant(0, captured) if is_sente else Elephant(1, captured)
            case _:
                return 0

    def __init__(self, owner, captured=False):
        if not (type(owner) is int):
            raise TypeError
        elif owner > 1:
            raise ValueError
        self.captured = captured
        self.owner = owner
        self.movable = [[0, 0, 0],
                        [0, 0, 0],
                        [0, 0, 0]]

    def serialize(self):
        is_sente = (self.owner == 0)
        char = self.__class__.__name__[0]
        return char if is_sente else char.lower()

    def print_movables(self):
        m = ''
        for li in self.movable:
            for i in li:
                m += str(i)
        return f'{m}'

    def add_captured(self):
        self.owner = 0 if self.owner else 1
        self.captured = True
        if (type(self) is Chick):
            self.promoted = False
            self.owner_movable()

    def remove_captured(self):
        self.captured = False
        return self

    def __eq__(self, other) -> bool:
        if not (type(self) is type(other)):
            return False
        return self.captured == other.captured and\
            self.movable == other.movable and\
            self.owner == other.owner

    def __ne__(self, other) -> bool:
        return not self == other


# Chick
class Chick(Piece):
    def __init__(self, owner, captured=False):
        super().__init__(owner)
        self.captured = captured
        self.promoted = False
        self.owner_movable()

    def __eq__(self, other) -> bool:
        if not (type(self) is type(other)):
            return False
        return self.captured == other.captured and\
               self.movable == other.movable and\
               self.owner == other.owner and\
               self.promoted == other.promoted

    def change_promoted(self):
        self.promoted = False if self.promoted else True
        self.owner_movable()

    def owner_movable(self):
        if self.promoted:
            if self.owner:
                self.movable = [[0, 1, 0],
                                [1, 0, 1],
                                [1, 1, 1]]
            else:
                self.movable = [[1, 1, 1],
                                [1, 0, 1],
                                [0, 1, 0]]
            return
        if self.owner:
            self.movable = [[0, 0, 0],
                            [0, 0, 0],
                            [0, 1, 0]]
        else:
            self.movable = [[0, 1, 0],
                            [0, 0, 0],
                            [0, 0, 0]]

    def serialize(self):
        # hardcoded Promoted Chick Char
        is_sente = not self.owner
        if self.promoted:
            return "P" if is_sente else "p"
        else:
            return "C" if is_sente else "c"

# Lion
class Lion(Piece):
    def __init__(self, owner, captured=False):
        super().__init__(owner, captured)
        self.movable = [[1, 1, 1],
                        [1, 0, 1],
                        [1, 1, 1]]


# Giraffe
class Giraffe(Piece):
    def __init__(self, owner, captured=False):
        super().__init__(owner, captured)
        self.movable = [[0, 1, 0],
                        [1, 0, 1],
                        [0, 1, 0]]


# Elephant
class Elephant(Piece):
    def __init__(self, owner, captured=False):
        super().__init__(owner, captured)
        self.movable = [[1, 0, 1],
                        [0, 0, 0],
                        [1, 0, 1]]
