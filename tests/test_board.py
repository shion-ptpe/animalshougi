import pytest
from animalshougi.piece import *
from animalshougi.board import Board
import itertools


board_a_turn_piece_indexes: set[tuple[int, int]] = {(1, 2), (0, 3), (1, 3), (2, 3)}
board_b_turn_piece_indexes: set[tuple[int, int]] = {(2, 0), (2, 1), (0, 2), 0}

@pytest.fixture
def boards():
    a = Board()
    a.board = [[Piece.deserialize("g"), Piece.deserialize("l"), Piece.deserialize("e")],
               [0, Piece.deserialize("c"), 0],
               [0, Piece.deserialize("C"), 0],
               [Piece.deserialize("E"), Piece.deserialize("L"), Piece.deserialize("G")]]
    a.selected_piece_pos()
    assert a.board == [[Giraffe(1),  Lion(1), Elephant(1)],
                       [         0, Chick(1),           0],
                       [         0, Chick(0),           0],
                       [Elephant(0), Lion(0),  Giraffe(0)]]

    assert board_a_turn_piece_indexes == {(1, 2), (0, 3), (1, 3), (2, 3)}

    b = Board()
    b.sente.add_captured(Piece.deserialize("e"))
    b.sente.add_captured(Piece.deserialize("g"))
    b.gote.add_captured(Piece.deserialize("G"))
    b.board = [[0, 0, Piece.deserialize("l")],
               [0, Piece.deserialize("C"), Piece.deserialize("e")],
               [Piece.deserialize("c"), 0, Piece.deserialize("L")],
               [0, 0, 0]]
    b.selected_piece_pos()
    b.toggle_turn()
    b.turn_piece_iter = itertools.cycle(iter(b.turn_piece_indexes))
    b.select_next_piece()

    assert b.board == [[       0,        0,     Lion(1)],
                       [       0, Chick(0), Elephant(1)],
                       [Chick(1),        0,     Lion(0)],
                       [       0,        0,           0]]

    assert board_b_turn_piece_indexes == {(2, 0), (2, 1), (0, 2), 0}

    assert b.select_movelists == [(0, 0), (1, 0), (0, 1), (1, 2), (0, 3), (1, 3), (2, 3), 0]

    return (a, b)


def test_board_eq(boards):
    af, bf = boards
    assert af != 1
    assert af != bf

    a = Board()
    a.board = [[Piece.deserialize("g"), Piece.deserialize("l"), Piece.deserialize("e")],
               [0, Piece.deserialize("c"), 0],
               [0, Piece.deserialize("C"), 0],
               [Piece.deserialize("E"), Piece.deserialize("L"), Piece.deserialize("G")]]

    assert af == a


def test_board_serialize(boards):
    a, b = boards

    assert a.serialize() == "SENTE\n\ngle\n-c-\n-C-\nELG"
    assert b.serialize() == "GOTE\nEGg\n--l\n-Ce\nc-L\n---"
    # assert Board().serialize() == "SENTE\n\n---\n---\n---\n---"


def test_view(boards):
    a, b = boards

    assert a.view() == "gle\n-c-\n-C-\nELG\n\n: SENTE (teban) \n: GOTE\n"
    assert b.view() == "--l\n-Ce\nc-L\n---\n\nEG: SENTE\ng: GOTE (teban) \n"

def test_str(boards):
    a, b = boards

    assert a.__str__() == "gle\n-c-\n-C-\nELG"
    assert b.__str__() == "--l\n-Ce\nc-L\n---"


def test_board_deserialize(boards):
    a, b = boards
    with pytest.raises(TypeError):
        _ = Board.deserialize(1)

    with pytest.raises(ValueError):
        _ = Board.deserialize("someinvalidstring")

    assert Board.deserialize(a.serialize()) == a
    assert Board.deserialize(b.serialize()) == b


def test_get_turn_pos(boards):
    a, b = boards
    assert a.get_turn_pos() == [[0, 0, 0],
                                [0, 0, 0],
                                [0, 1, 0],
                                [1, 1, 1]]
    assert b.turn == 1
    assert b.get_turn_pos() == [[0, 0, 1],
                                [0, 0, 1],
                                [1, 0, 0],
                                [0, 0, 0]]


def test_selected_piece_pos(boards):
    a, b = boards
    assert board_a_turn_piece_indexes == {(1, 2), (0, 3), (1, 3), (2, 3)}
    assert a.selected_pos == (2, 3)
    assert a.selected_piece_piece == (2, 3)

    a.select_next_piece()  # Space key
    assert a.selected_pos == (1, 2)
    assert a.selected_piece_piece == (1, 2)

    a.select_next_move_piece()  # Enter key
    a.select_movelists == [(1, 1), (1, 2)]
    assert a.selected_pos == (1, 1)
    assert a.selected_move_piece == (1, 1)


def test_select_next_piece(boards):
    a, b = boards
    assert board_a_turn_piece_indexes == {(1, 2), (0, 3), (1, 3), (2, 3)}
    assert a.selected_pos == (2, 3)
    a.select_next_piece()
    assert a.selected_pos == (1, 2)
    a.select_next_piece()
    assert a.selected_pos == (1, 3)
    a.select_next_piece()
    assert a.selected_pos == (0, 3)
    a.select_next_piece()
    assert a.selected_pos == (2, 3)

    assert board_b_turn_piece_indexes == {(2, 0), (2, 1), (0, 2), 0}
    assert b.selected_piece_piece == 0

    assert b.select_movelists == [(0, 0), (1, 0), (0, 1), (1, 2), (0, 3), (1, 3), (2, 3), 0]

    assert b.selected_pos == 0
    b.select_next_piece()
    assert b.selected_pos == (0, 2)


def test_selected_move_iter(boards):
    a, b = boards
    a.selected_piece_piece = (2, 3)  # G
    a.selected_move_iter()
    assert a.select_movelists == [(2, 2), (2, 3)]
    a.selected_piece_piece = (1, 3)  # L
    a.selected_move_iter()
    assert a.select_movelists == [(0, 2), (2, 2), (1, 3)]
    b.selected_piece_piece = (0)  # G
    b.selected_move_iter()
    assert b.select_movelists == [(0, 0), (1, 0), (0, 1), (1, 2), (0, 3), (1, 3), (2, 3), 0]


def test_select_next_move_piece(boards):
    a, b = boards
    a.selected_piece_piece = (2, 3)  # G
    a.select_next_move_piece()
    a.selected_pos = (2, 2)
    a.select_next_move_piece()
    a.selected_pos = (2, 3)


def test_boollist_to_indexlist(boards):
    a, b = boards
    assert a.boollist_to_indexlist(a.get_turn_pos()) == [
        (1, 2), (0, 3), (1, 3), (2, 3)]
    assert a.movable_list == [0, 0, 0, 0,
                              0, 0, 0, 1, 0, 1, 1, 1]
    assert a.indexlist == [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1),
                           (2, 1), (0, 2), (1, 2), (2, 2), (0, 3), (1, 3), (2, 3)]
    assert b.boollist_to_indexlist(b.get_turn_pos()) == [
        (2, 0), (2, 1), (0, 2)]


def test_is_original_pos(boards):
    a, b = boards
    # a.select_next_piece()
    assert a.selected_pos == (2, 3)
    assert a.selected_piece_piece == (2, 3)
    a.select_next_move_piece()
    assert a.select_movelists == [(2, 2), (2, 3)]
    assert a.selected_move_piece == (2, 2)
    assert a.is_original_pos() == False
    a.select_next_move_piece()
    assert a.selected_move_piece == (2, 3)
    assert a.is_original_pos() == True


def test_turn_piece_indexes(boards):
    a, b = boards
    assert a.turn_piece_indexes == board_a_turn_piece_indexes
    assert b.turn_piece_indexes == board_b_turn_piece_indexes


def test_get_legal_moves(boards):
    a, b = boards

    assert a.serialize() == "SENTE\n\ngle\n-c-\n-C-\nELG"
    assert b.serialize() == "GOTE\nEGg\n--l\n-Ce\nc-L\n---"

    """
    SENTE
    gle
    -c-
    -C-
    ELG
    """

    assert a.get_legal_moves((0, 3)) == [[0, 0, 0],
                                            [0, 0, 0],
                                            [0, 0, 0],
                                            [0, 0, 0]]

    assert a.get_legal_moves((1, 3)) == [[0, 0, 0],
                                            [0, 0, 0],
                                            [1, 0, 1],
                                            [0, 0, 0]]

    assert a.get_legal_moves((1, 2)) == [[0, 0, 0],
                                            [0, 1, 0],
                                            [0, 0, 0],
                                            [0, 0, 0]]

    with pytest.raises(ValueError):
        a.get_legal_moves((0, 2))
        a.get_legal_moves((1, 1))
        a.get_legal_moves(0)
    """
    GOTE EGg
    --l
    -Ce
    c-L
    ---
    """

    assert b.get_legal_moves((0, 2)) == [[0, 0, 0],
                                            [0, 0, 0],
                                            [0, 0, 0],
                                            [1, 0, 0]]

    assert b.get_legal_moves((2, 1)) == [[0, 1, 0],
                                            [0, 0, 0],
                                            [0, 1, 0],
                                            [0, 0, 0]]

    assert b.get_legal_moves(0) == [[1, 1, 0],
                                       [1, 0, 0],
                                       [0, 1, 0],
                                       [1, 1, 1]]

    with pytest.raises(ValueError):
        b.get_legal_moves((0, 3))
        b.get_legal_moves((1, 2))
        b.get_legal_moves(2)


def test_can_move(boards):
    a, b = boards
    assert a.can_move((1, 3), (0, 2))
    assert a.can_move((2, 3), (2, 2))
    assert not a.can_move((0, 3), (0, 2))

    assert b.can_move(0, (1, 2))
    assert not b.can_move(0, (0, 2))


def test_move_piece():
    a = Board.deserialize("SENTE\n\ngle\n-c-\n-C-\nELG")
    b = Board.deserialize("GOTE\nEGg\n--l\n-Ce\nc-L\n---")
    c = Board.deserialize("SENTE\nC\ng-e\nlC-\n---\nELG")
    a_cp = Board.deserialize("SENTE\n\ngle\n-c-\n-C-\nELG")

    # 後手のcをとる動き
    a.move_piece((1, 2), (1, 1))
    assert a.serialize() == "SENTE\nC\ngle\n-C-\n---\nELG"  # 指した後の盤の状態

    # eを動かす
    b.move_piece((2, 1), (1, 2))
    assert b.serialize() == "GOTE\nEGg\n--l\n-C-\nceL\n---"

    # cを敵陣に動かす
    c.move_piece((1, 1), (1, 0))
    assert c.serialize() == "SENTE\nC\ngPe\nl--\n---\nELG"

    with pytest.raises(ValueError):
        a.turn = 0; a.move_piece((0, 2), (0, 1))  # 存在しない駒を動かそうとする
        a_cp.turn = 0; a_cp.move_piece((0, 0), (0, 0))  # 動けない範囲に動かそうとする
        b.turn = 1; b.move_piece(0, (2, 0))       # 動けない範囲に動かそうとする

def test_move_piece__case_captured():
    a = Board.deserialize("SENTE\n\ngle\n-c-\n-C-\nELG")
    b = Board.deserialize("GOTE\nEGg\n--l\n-Ce\nc-L\n---")

    # 持ち駒のgを打つ
    b.move_piece(0, (0, 3))
    assert b.serialize() == "GOTE\nEG\n--l\n-Ce\nc-L\ng--"
    b.toggle_turn()

    # 持ち駒のGを打つ
    b.move_piece(1, (1, 3))
    assert b.serialize() == "SENTE\nE\n--l\n-Ce\nc-L\ngG-"

    with pytest.raises(ValueError):
        a.move_piece(1, (0, 1))


def test_get_piece(boards):
    a, b = boards
    assert a.get_piece((0, 3)).serialize() == "E"
    assert a.get_piece((1, 3)).serialize() == "L"

    assert b.get_piece(0).serialize() == "g"

    with pytest.raises(ValueError):
        a.get_piece((0, 2))
        b.get_piece(1)


def test_replace_piece():
    a = Board.deserialize("SENTE\n\ngle\n-c-\n-C-\nELG")
    b = Board.deserialize("GOTE\nEGg\n--l\n-Ce\nc-L\n---")

    a.replace_piece((0, 3), 0)
    assert a.serialize() == "SENTE\n\ngle\n-c-\n-C-\n-LG"

    b.replace_piece((0, 2), 0)
    assert b.serialize() == "GOTE\nEGg\n--l\n-Ce\n--L\n---"


def test_toggle_turn(boards):
    a, b = boards

    a.toggle_turn()
    assert a.serialize() == "GOTE\n\ngle\n-c-\n-C-\nELG"

    b.toggle_turn()
    assert b.serialize() == "SENTE\nEGg\n--l\n-Ce\nc-L\n---"

    assert next(a.turn_piece_iter) == (1, 0)
    assert next(b.turn_piece_iter) == 0
    assert next(b.turn_piece_iter) == 1
    assert next(b.turn_piece_iter) == (1, 1)
    assert next(b.turn_piece_iter) == (2, 2)
