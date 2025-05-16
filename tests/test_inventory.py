"""
Test suite for inventory management system.
Author: Deny Mudashiru
Date: 2024
"""

import unittest
from src.inventory import Inventory, Item

class TestInventory(unittest.TestCase):
    """Test cases for inventory management."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.inventory = Inventory()
        self.health_potion = Item("Health Potion", "Consumable", 10)
        self.weapon = Item("Sword", "Weapon", 20)
        self.armor = Item("Shield", "Armor", 15)

    def test_inventory_creation(self):
        """Test inventory initialization."""
        self.assertEqual(len(self.inventory.items), 0)
        self.assertIsInstance(self.inventory.items, list)

    def test_add_item(self):
        """Test adding items to inventory."""
        self.inventory.add_item(self.health_potion)
        self.assertEqual(len(self.inventory.items), 1)
        self.assertEqual(self.inventory.items[0].name, "Health Potion")
        
        # Test adding multiple items
        self.inventory.add_item(self.weapon)
        self.inventory.add_item(self.armor)
        self.assertEqual(len(self.inventory.items), 3)

    def test_item_properties(self):
        """Test item property access."""
        self.inventory.add_item(self.health_potion)
        item = self.inventory.items[0]
        self.assertEqual(item.name, "Health Potion")
        self.assertEqual(item.type, "Consumable")
        self.assertEqual(item.value, 10)

    def test_inventory_limits(self):
        """Test inventory capacity limits."""
        # Add multiple items
        for _ in range(20):
            self.inventory.add_item(self.health_potion)
        self.assertLessEqual(len(self.inventory.items), 20)

    def test_item_types(self):
        """Test different item types in inventory."""
        self.inventory.add_item(self.health_potion)
        self.inventory.add_item(self.weapon)
        self.inventory.add_item(self.armor)
        
        # Verify item types
        item_types = [item.type for item in self.inventory.items]
        self.assertIn("Consumable", item_types)
        self.assertIn("Weapon", item_types)
        self.assertIn("Armor", item_types)

    def test_item_values(self):
        """Test item value assignments."""
        self.inventory.add_item(self.health_potion)
        self.inventory.add_item(self.weapon)
        
        # Verify item values
        for item in self.inventory.items:
            if item.name == "Health Potion":
                self.assertEqual(item.value, 10)
            elif item.name == "Sword":
                self.assertEqual(item.value, 20)

if __name__ == "__main__":
    unittest.main()
