class Piece:
    @classmethod
    def deserialize(cls, str):
        return cls(str)

    def __init__(self, char) -> None:
        self.char = char

    def serialize(self) -> str:
        return self.char
