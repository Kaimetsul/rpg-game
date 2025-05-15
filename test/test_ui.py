import pygame
import pytest
from src.RPG import button_positions, button_texts

# Initialize pygame for testing
pygame.init()

def test_button_positions():
    # Check if the number of button positions matches the number of button texts
    assert len(button_positions) == len(button_texts), "Number of button positions should match number of button texts"

def test_button_texts():
    # Check if the button texts are as expected
    expected_texts = ["Hunter", "Mage", "Tank", "Beast Tamer"]
    assert button_texts == expected_texts, "Button texts should match the expected values"

# Clean up pygame
pygame.quit() 