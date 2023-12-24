import pytest
from tribe import Tribe, TribeFactory


def test_create_tribe():
    tf = TribeFactory()
    tribe = tf.create_empty_tribe()
    assert tribe.color
    assert len(tribe.players) == 0


def test_create_many_tribes():
    tf = TribeFactory()
    tribes = []
    num_tribes_to_create = 15

    for _ in range(num_tribes_to_create):
        tribe = tf.create_empty_tribe()
        assert tribe.color
        assert len(tribe.players) == 0
        tribes.append(tribe)

    assert len(tribes) == num_tribes_to_create


def test_create_too_many_tribes():
    tf = TribeFactory()
    tribes = []
    num_tribes_to_create = 15

    for _ in range(num_tribes_to_create):
        tribe = tf.create_empty_tribe()
        assert tribe.color
        assert len(tribe.players) == 0
        tribes.append(tribe)

    with pytest.raises(ValueError):
        tribe = tf.create_empty_tribe()
        tribes.append(tribe)
