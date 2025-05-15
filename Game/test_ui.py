import pytest
from Game.ui import Game

def test_game_initialization():
    game = Game()
    assert game is not None

def test_game_start():
    game = Game()
    # Add more specific tests based on your UI implementation
    assert hasattr(game, 'start') 