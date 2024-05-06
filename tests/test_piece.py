import pytest
from animalshougi.piece import Piece
from animalshougi.player import Player
from animalshougi.piece import Chick
from animalshougi.piece import Lion
from animalshougi.piece import Giraffe
from animalshougi.piece import Elephant


sente, gote = [0, 1]


@pytest.fixture
def mts():
    return [Piece(sente), Piece(gote)]


@pytest.fixture
def ck():
    return [Chick(sente), Chick(gote)]


@pytest.fixture
def cpcs():
    return [Chick(sente), Chick(gote),
            Lion(sente), Lion(gote),
            Giraffe(sente), Giraffe(gote),
            Elephant(sente), Elephant(gote)]


def test_init(mts):
    a, b = mts
    assert a.captured == False
    assert a.owner == sente
    assert a.movable == [[0, 0, 0],
                         [0, 0, 0],
                         [0, 0, 0]]
    assert b.captured == False
    assert b.owner == gote
    assert b.movable == [[0, 0, 0],
                         [0, 0, 0],
                         [0, 0, 0]]
    with pytest.raises(TypeError):
        _ = Piece(Player())
    with pytest.raises(ValueError):
        _ = Piece(2)


def test_print_movables(mts):
    a, b = mts
    assert a.print_movables() == '000000000'
    assert b.print_movables() == '000000000'


def test_add_captured(mts):
    a, b = mts
    a.add_captured()
    assert a.captured == True
    assert a.owner == gote
    a.add_captured()
    assert a.captured == True
    assert a.owner == sente

    c = Chick(gote)
    c.change_promoted()
    c.add_captured()
    assert c.captured == True
    assert c.promoted == False
    assert c.owner == sente


def test_remove_captured(mts):
    a, b = mts
    a.add_captured()  # a.captured == True , a.owner == you
    a.remove_captured()
    assert a.captured == False
    assert a.owner == gote


def test_inits():
    c = Chick(sente)
    c2 = Chick(gote)
    l = Lion(sente)
    l2 = Lion(gote)
    g = Giraffe(sente)
    g2 = Giraffe(gote)
    e = Elephant(sente)
    e2 = Elephant(gote)

    assert c.captured == False
    assert c.owner == sente
    assert c.movable == [[0, 1, 0],
                         [0, 0, 0],
                         [0, 0, 0]]
    assert c.promoted == False
    assert c2.captured == False
    assert c2.owner == gote
    assert c2.movable == [[0, 0, 0],
                          [0, 0, 0],
                          [0, 1, 0]]
    assert c2.promoted == False

    assert l.captured == False
    assert l.owner == sente
    assert l.movable == [[1, 1, 1],
                         [1, 0, 1],
                         [1, 1, 1]]
    assert l2.captured == False
    assert l2.owner == gote
    assert l2.movable == [[1, 1, 1],
                          [1, 0, 1],
                          [1, 1, 1]]

    assert g.captured == False
    assert g.owner == sente
    assert g.movable == [[0, 1, 0],
                         [1, 0, 1],
                         [0, 1, 0]]
    assert g2.captured == False
    assert g2.owner == gote
    assert g2.movable == [[0, 1, 0],
                          [1, 0, 1],
                          [0, 1, 0]]

    assert e.captured == False
    assert e.owner == sente
    assert e.movable == [[1, 0, 1],
                         [0, 0, 0],
                         [1, 0, 1]]
    assert e2.captured == False
    assert e2.owner == gote
    assert e2.movable == [[1, 0, 1],
                          [0, 0, 0],
                          [1, 0, 1]]


def test_change_promoted(ck):
    a, b = ck
    a.change_promoted()
    a.promoted = True
    a.movable = [[1, 1, 1],
                 [1, 0, 1],
                 [0, 1, 0]]

    a.change_promoted()
    a.promoted = False
    a.movable = [[0, 1, 0],
                 [0, 0, 0],
                 [0, 0, 0]]


def test_serialize():
    assert Chick(0).serialize() == "C"
    assert Chick(1).serialize() == "c"

    p_chick = Chick(0)
    p_chick.promoted = True
    assert p_chick.serialize() == "P"
    p_chick.owner = 1
    assert p_chick.serialize() == "p"

    assert Lion(0).serialize() == "L"
    assert Lion(1).serialize() == "l"

    assert Giraffe(0).serialize() == "G"
    assert Giraffe(1).serialize() == "g"

    assert Elephant(0).serialize() == "E"
    assert Elephant(1).serialize() == "e"


def test_deserialize():
    with pytest.raises(TypeError):
        _ = Piece.deserialize(1)

    with pytest.raises(ValueError):
        _ = Piece.deserialize("CC")

    assert Piece.deserialize("C") == Chick(0)
    assert Piece.deserialize("c") == Chick(1)

    assert Piece.deserialize("L") == Lion(0)
    assert Piece.deserialize("l") == Lion(1)

    assert Piece.deserialize("G") == Giraffe(0)
    assert Piece.deserialize("g") == Giraffe(1)

    assert Piece.deserialize("E") == Elephant(0)
    assert Piece.deserialize("e") == Elephant(1)

    assert Piece.deserialize("e") != Giraffe(1)
    assert Piece.deserialize("C") != Chick(1)


def test_eq():
    assert Chick(0) == Chick(0)
    assert Lion(0) == Lion(0)

    assert Elephant(0) != Elephant(1)
    assert Giraffe(0) != Giraffe(1)

    assert Chick(0) != Lion(0)
    assert Giraffe(0) != Elephant(0)
