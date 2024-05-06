import re
import numpy as np
import itertools
from animalshougi.piece import *
from animalshougi.player import Player

class Board:
    @classmethod
    def deserialize(cls, string: str):
        if type(string) is not str:
            raise TypeError
        if not re.fullmatch(r"(?:SENTE|GOTE)\n[CEGLcegl]*\n(?:[-CEGLcegl]{3}\n){3}[-CEGLcegl]{3}", string):
            raise ValueError

        board = cls()
        for i, line in enumerate(string.split("\n")):
            if i == 0:
                board.turn = 0 if line == "SENTE" else 1
            elif i == 1:  # motigoma
                for char in line:
                    if char == char.upper():
                        board.sente.captured_piece.append(Piece.deserialize(char, captured=True))
                    else:
                        board.gote.captured_piece.append(Piece.deserialize(char, captured=True))
            else:  # bannmenn
                for j, char in enumerate(line):
                    board.board[i - 2][j] = Piece.deserialize(char)
        return board

    def __init__(self):
        self.board: list[list[int | Piece]] = \
                   [[Giraffe(1),  Lion(1), Elephant(1)],
                    [         0, Chick(1),           0],
                    [         0, Chick(0),           0],
                    [Elephant(0), Lion(0),  Giraffe(0)]]
        self.players = [Player(), Player()]
        self.sente = self.players[0]
        self.gote = self.players[1]
        self.turn: int = 0

    def __eq__(self, other):
        if not isinstance(other, Board):
            return False

        return self.serialize() == other.serialize()

    def serialize(self) -> str:
        turn_string = "SENTE" if self.turn == 0 else "GOTE"
        captureds_string = "".join(player.serialize()
                                   for player in self.players)
        board_string = "\n".join(
            ["".join(
                [piece.serialize() if piece else "-" for piece in line])
                for line in self.board])
        return turn_string + "\n" + captureds_string + "\n" + board_string

    def view(self):
        message = []
        message.append("\n".join(
            ["".join(
                [piece.serialize() if piece else "-" for piece in line])
                for line in self.board]))
        message.append("\n\n")
        for turn, player in enumerate(self.players):
            message.append("".join(player.serialize()))  # captureds_string
            message.append(": SENTE" if turn == 0 else ": GOTE")  # turn_string
            if self.turn == turn:
                message.append(" (teban) ")
            message.append('\n')
        return "".join(message)

    def __str__(self):
        return  "\n".join(
                ["".join(
                    [piece.serialize() if piece else "-" for piece in line])
                    for line in self.board])

    @property
    def turn_player(self):
        return self.players[self.turn]

    # 味方の駒をTrueにしたリストを返す
    def get_turn_pos(self):
        output = [[], [], [], []]
        for i in range(4):
            for j in range(3):
                piece = self.board[i][j]
                if piece == 0:
                    output[i].append(0)
                elif piece.owner == self.turn:
                    output[i].append(1)
                else:
                    output[i].append(0)
        return output

    @property
    def turn_piece_binary_list(self):
        return self.get_turn_pos()

    @property
    def turn_piece_indexes(self) -> set[tuple[int, int] | int]:
        piece_index_set: set[tuple[int, int] | int] = set()
        # 盤上の駒
        for y, x_line in enumerate(self.turn_piece_binary_list):
            for x, piece_exist in enumerate(x_line):
                if piece_exist:
                    piece_index_set.add((x, y))
        # 持ち駒
        for i, _ in enumerate(self.turn_player.captured_piece):
            piece_index_set.add(i)

        return piece_index_set

    # 駒選択前の動ける範囲のインデックスリストから一つ値を取り出す
    def selected_piece_pos(self):
        try:
            return self.selected_pos
        except:
            self.turn_piece_iter = itertools.cycle(iter(self.turn_piece_indexes))
            self.select_next_piece()
            return self.selected_pos

    # 呼び出すたびにselected_piece_posで返す値が変わる
    def select_next_piece(self):
        self.selected_pos = next(self.turn_piece_iter)
        self.selected_piece_piece = self.selected_move_piece  = self.selected_pos
        self.selected_move_iter()

    # 駒選択後の動ける範囲のインデックスリストから一つ値を取り出す
    def selected_move_iter(self):
        self.select_movelists = self.boollist_to_indexlist(self.get_legal_moves(self.selected_piece_piece))
        self.select_movelists.append(self.selected_piece_piece)
        self.move_piece_iter = itertools.cycle(iter(self.select_movelists))
        return self.move_piece_iter


    # 呼び出すたびにselected_move_posで返す値が変わる
    def select_next_move_piece(self):
        self.selected_pos = next(self.move_piece_iter)
        self.selected_move_piece = self.selected_pos

    # 受け取ったboolリストのtrue部分をインデックスリストにする
    def boollist_to_indexlist(self, bool_lists):
        self.bool_lists = bool_lists
        self.movable_list = sum(self.bool_lists, [])
        self.indexlist = [(x, y) for y in range(len(self.bool_lists))
                          for x in range(len(self.bool_lists[3]))]
        self.piece_index_list = []
        for index, movable in enumerate(self.movable_list):
            if movable:
                self.piece_index_list.append(self.indexlist[index])
        return self.piece_index_list

    # selected_piece_posで選択された駒とselected_move_pieceを比較する
    def is_original_pos(self):
        return self.selected_piece_piece == self.selected_move_piece

    # todo (優先度低): 王手の時の処理
    def get_legal_moves(self, pos: tuple[int, int] | int):
        if pos not in self.turn_piece_indexes:
            raise ValueError("no piece at given pos")

        if isinstance(pos, int):
            _ = self.turn_player.captured_piece[pos]
            return np.logical_not(np.array(self.board)).tolist()

        x, y = pos
        target_piece = self.board[y][x]

        # 4行3列行列(board)から上下左右に1行1列ずつ追加したzerosをbool行列にし、これを操作してlegal_movesを求める
        # 最後に、int行列に変換後、追加した行/列を消去して、3*4に直して返す
        legal_moves_6x5 = np.zeros((6, 5), dtype=bool)

        piece_movable_area = np.array(target_piece.movable, dtype=bool)
        # 駒の能力的に移動できる箇所のみ1にする
        legal_moves_6x5[y:y+3, x:x+3] = legal_moves_6x5[y:y+3, x:x+3] | piece_movable_area

        # 味方の駒がない場所に絞り込む。能力的に移動可能かをA, 味方の駒をBとすると、A=1 && B=0の時にのみ1になれば良い。
        # => A & ~B でOK。
        legal_moves_6x5[1:5, 1:4] = legal_moves_6x5[1:5, 1:4] & ~np.array(self.turn_piece_binary_list, dtype=bool)

        # 3*4リストに直してreturn
        return np.array(legal_moves_6x5[1:5, 1:4], dtype=int).tolist()

    def can_move(self, original, dist):
        x, y = dist
        return self.get_legal_moves(original)[y][x]

    # 駒を動かすが、ターンは変えない
    def move_piece(self, origin: tuple[int, int] | int, dest: tuple[int, int]):
        if ((origin not in self.turn_piece_indexes) or
            not self.can_move(origin, dest)):
            raise ValueError("駒が存在していないか、指定した座標に駒を移動することができません。")

        origin_piece = self.get_piece(origin)
        dest_piece = self.get_piece(dest)

        # 持ち駒を打つ場合
        if isinstance(origin, int):
            self.replace_piece(dest, origin_piece.remove_captured())
            self.turn_player.remove_captured(origin)
            return
        # ひよこが相手陣地にいるか
        elif (type(origin_piece) == Chick and
              origin_piece.promoted == False and
              dest[1] == origin_piece.owner * 3):
            origin_piece.change_promoted()

        # 行き先に駒が存在するなら、適切なplayerの持ち駒にあった駒を加える
        if dest_piece:
            self.turn_player.add_captured(dest_piece)
            self.replace_piece(dest, origin_piece)
            self.replace_piece(origin, 0)
        # 行き先に駒が存在しないなら、単に駒を移動する
        else:
            self.replace_piece(dest, origin_piece)
            self.replace_piece(origin, 0)

    def get_piece(self, pos: tuple[int, int] | int):
        if isinstance(pos, int):
            try:
                return self.turn_player.captured_piece[pos]
            except IndexError:
                raise ValueError("such captured piece does not exist")
        x, y = pos
        return self.board[y][x]

    def replace_piece(self, pos: tuple[int, int], to) -> None:
        x, y = pos
        self.board[y][x] = to

    def toggle_turn(self):
        self.turn = 0 if self.turn else 1
        self.turn_piece_iter = itertools.cycle(iter(self.turn_piece_indexes))
        try:
            del self.selected_pos
        except:
            pass
