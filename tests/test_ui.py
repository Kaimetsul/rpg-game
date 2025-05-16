"""
Test 
Author: Deny Mudashiru
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock pygame.display.set_mode to avoid the "No available video device" error
import pygame
pygame.display.set_mode = lambda *args, **kwargs: None

import src.main

def test_import_main():
    import src.main 