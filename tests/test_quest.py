"""
Test suite for quest management system.
Author: Deny Mudashiru
Date: 2024
"""

import unittest
from src.quest import Quest, QuestManager

class TestQuest(unittest.TestCase):
    """Test cases for quest system."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.quest_manager = QuestManager()
        self.ogre_quest = Quest(
            "Defeat the Ogre",
            "Slay the ogre terrorizing the village",
            ["Kill 3 enemies", "Collect ogre teeth"],
            reward={"gold": 200, "experience": 100}
        )
        self.collection_quest = Quest(
            "Gather Resources",
            "Collect resources for the village",
            ["Gather 5 herbs", "Find 3 crystals"],
            reward={"gold": 100, "experience": 50}
        )

    def test_quest_creation(self):
        """Test quest initialization and properties."""
        self.assertEqual(self.ogre_quest.title, "Defeat the Ogre")
        self.assertEqual(self.ogre_quest.description, "Slay the ogre terrorizing the village")
        self.assertEqual(len(self.ogre_quest.objectives), 2)
        self.assertEqual(self.ogre_quest.reward["gold"], 200)

    def test_quest_manager(self):
        """Test quest manager functionality."""
        # Test adding quests
        self.quest_manager.add_quest(self.ogre_quest)
        self.assertEqual(len(self.quest_manager.get_active_quests()), 1)
        
        # Test adding multiple quests
        self.quest_manager.add_quest(self.collection_quest)
        self.assertEqual(len(self.quest_manager.get_active_quests()), 2)

    def test_quest_completion(self):
        """Test quest completion mechanics."""
        self.quest_manager.add_quest(self.ogre_quest)
        
        # Test quest not completed initially
        self.assertFalse(self.ogre_quest.is_completed())
        
        # Test quest completion
        self.ogre_quest.complete()
        self.assertTrue(self.ogre_quest.is_completed())

    def test_quest_objectives(self):
        """Test quest objective tracking."""
        self.assertEqual(len(self.ogre_quest.objectives), 2)
        self.assertIn("Kill 3 enemies", self.ogre_quest.objectives)
        self.assertIn("Collect ogre teeth", self.ogre_quest.objectives)

    def test_quest_rewards(self):
        """Test quest reward system."""
        self.assertEqual(self.ogre_quest.reward["gold"], 200)
        self.assertEqual(self.ogre_quest.reward["experience"], 100)
        
        self.assertEqual(self.collection_quest.reward["gold"], 100)
        self.assertEqual(self.collection_quest.reward["experience"], 50)

    def test_quest_manager_operations(self):
        """Test quest manager operations."""
        # Add quests
        self.quest_manager.add_quest(self.ogre_quest)
        self.quest_manager.add_quest(self.collection_quest)
        
        # Test getting active quests
        active_quests = self.quest_manager.get_active_quests()
        self.assertEqual(len(active_quests), 2)
        
        # Test quest completion affects active quests
        self.ogre_quest.complete()
        self.quest_manager.complete_quest(self.ogre_quest.title)  # Explicitly complete the quest
        active_quests = self.quest_manager.get_active_quests()
        self.assertEqual(len(active_quests), 1)

if __name__ == "__main__":
    unittest.main()
