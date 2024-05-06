import pytest
from animalshougi.player import Player
from animalshougi.piece import *


@pytest.fixture
def mts():
    return (Player(), Player())


cap_C0  = Chick(0)
cap_G0 = Giraffe(0)
cap_E0 = Elephant(0)
cap_L0 = Lion(0)
cap_c1 = Chick(1)
cap_g1 = Giraffe(1)
cap_e1 = Elephant(1)
cap_l1 = Lion(1)
namelist = [cap_C0, cap_G0, cap_E0, cap_L0, cap_c1, cap_g1, cap_e1, cap_l1]
for cap_piece in namelist:
    cap_piece.captured = True

def test_init(mts):
    a, b = mts

    assert a.captured_piece == []
    assert b.captured_piece == []


def test_serialize(mts):
    a,b = mts

    player_a = Player()
    player_b = Player()

    player_a.add_captured(Chick(1))
    player_a.add_captured(Elephant(1))
    player_b.add_captured(Giraffe(0))

    assert a.serialize() == ''
    assert b.serialize() == ''

    assert player_a.serialize() == "CE"
    assert player_b.serialize() == "g"

def test_add_captured(mts):
    a, b = mts
    with pytest.raises(TypeError):
        _ = Player().add_captured(1)
        _ = Player().add_captured('L')

    assert a.captured_piece == []
    a.add_captured(Chick(1))
    assert a.captured_piece == [cap_C0]
    a.add_captured(Giraffe(1))
    assert a.captured_piece == [cap_C0, cap_G0]
    a.add_captured(Giraffe(1))
    assert a.captured_piece == [cap_C0, cap_G0, cap_G0]
    a.add_captured(Chick(1))
    assert a.captured_piece == [cap_C0, cap_G0, cap_G0, cap_C0]
    a.add_captured(Elephant(1))
    assert a.captured_piece == [cap_C0, cap_G0, cap_G0, cap_C0, cap_E0]
    a.add_captured(Elephant(1))
    assert a.captured_piece == [cap_C0, cap_G0, cap_G0, cap_C0, cap_E0, cap_E0]
    a.add_captured(Lion(1))
    assert a.captured_piece == [cap_C0, cap_G0, cap_G0, cap_C0, cap_E0, cap_E0, cap_L0]

    assert b.captured_piece == []
    b.add_captured(Chick(0))
    assert b.captured_piece == [cap_c1]
    b.add_captured(Giraffe(0))
    assert b.captured_piece == [cap_c1, cap_g1]


def test_remove_captured(mts):
    a, b = mts
    with pytest.raises(TypeError):
        _ = Player.add_captured(1)
        _ = Player.add_captured('L')
    test_add_captured(mts)
    assert a.captured_piece == [cap_C0, cap_G0, cap_G0, cap_C0, cap_E0, cap_E0, cap_L0]
    a.remove_captured(3)
    assert a.captured_piece == [cap_C0, cap_G0, cap_G0, cap_E0, cap_E0, cap_L0]
    a.remove_captured(2)
    assert a.captured_piece == [cap_C0, cap_G0, cap_E0, cap_E0, cap_L0]
