class Player:
    def __init__(self) -> None:
        self.captured = []

    def add_captured(self, piece):
        self.captured.append(piece)

    def serialize(self):
        return "".join([piece.serialize() for piece in self.captured])
