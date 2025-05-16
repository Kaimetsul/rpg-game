"""
Test suite for game mechanics and character interactions.
Author: Deny Mudashiru
"""

import unittest
from src.game import Character, Battle

class TestGame(unittest.TestCase):
    """Test cases for core game mechanics."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.hunter = Character("Hunter", [
            {"name": "Arrow Shot", "damage": 50},
            {"name": "Precise Strike", "damage": 75}
        ])
        self.tank = Character("Tank", [
            {"name": "Shield Bash", "damage": 30},
            {"name": "Heavy Strike", "damage": 45}
        ])
        self.beast = Character("Beast", [
            {"name": "Claw Attack", "damage": 40},
            {"name": "Feral Strike", "damage": 60}
        ])

    def test_character_creation(self):
        """Test character creation with different classes."""
        self.assertEqual(self.hunter.name, "Hunter")
        self.assertEqual(len(self.hunter.attacks), 2)
        self.assertEqual(self.tank.name, "Tank")
        self.assertEqual(len(self.tank.attacks), 2)
        self.assertEqual(self.beast.name, "Beast")
        self.assertEqual(len(self.beast.attacks), 2)

    def test_attack_damage(self):
        """Test attack damage calculations and enemy HP reduction."""
        battle = Battle(self.hunter)
        initial_hp = battle.enemy_hp
        
        # Test first attack
        attack_name, damage, enemy_hp = battle.attack(0)
        self.assertEqual(attack_name, "Arrow Shot")
        self.assertEqual(damage, 50)
        self.assertEqual(enemy_hp, initial_hp - damage)
        
        # Test second attack
        attack_name, damage, enemy_hp = battle.attack(1)
        self.assertEqual(attack_name, "Precise Strike")
        self.assertEqual(damage, 75)

    def test_battle_mechanics(self):
        """Test battle mechanics including enemy defeat conditions."""
        battle = Battle(self.tank)
        
        # Test enemy not defeated
        battle.enemy_hp = 100
        self.assertFalse(battle.is_enemy_defeated())
        
        # Test enemy defeat
        battle.enemy_hp = 30
        battle.attack(0)  # Shield Bash should defeat enemy
        self.assertTrue(battle.is_enemy_defeated())

    def test_maze_progression(self):
        """Test maze progression and path tracking."""
        battle = Battle(self.beast)
        battle.enter_maze()
        
        # Test initial path
        self.assertEqual(len(battle.current_path), 0)
        
        # Test path progression
        self.assertTrue(battle.make_choice("left"))
        self.assertEqual(len(battle.current_path), 1)
        self.assertEqual(battle.current_path[0], "left")
        
        # Test path completion
        for _ in range(len(battle.correct_path) - 1):
            battle.make_choice("right")
        self.assertEqual(len(battle.current_path), len(battle.correct_path))

    def test_invalid_attack_index(self):
        """Test handling of invalid attack indices."""
        battle = Battle(self.hunter)
        with self.assertRaises(IndexError):
            battle.attack(5)  # Invalid attack index

    def test_character_stats(self):
        """Test character statistics and attributes."""
        self.assertEqual(self.hunter.attacks[0]["name"], "Arrow Shot")
        self.assertEqual(self.hunter.attacks[0]["damage"], 50)
        self.assertEqual(self.hunter.attacks[1]["name"], "Precise Strike")
        self.assertEqual(self.hunter.attacks[1]["damage"], 75)

if __name__ == "__main__":
    unittest.main() 