from animalshougi.piece import *

class Player:
    def __init__(self):
        self.captured_piece = []

    def serialize(self) -> str:
        return "".join(piece.serialize() for piece in self.captured_piece)

    def add_captured(self, piece):  # pieceの中身は"Pieceクラス"
        if not type(piece) in (Chick, Giraffe, Elephant, Lion, Piece):
            raise TypeError
        piece.add_captured()
        self.captured_piece.append(piece)
        # コマを持ち駒に加える
        # 鶏はひよこに直す

    def remove_captured(self, index):  # pieceの中身は"Pieceクラス"
        self.captured_piece[index].remove_captured()
        self.captured_piece.pop(index)
        # コマを待ち駒から出す
