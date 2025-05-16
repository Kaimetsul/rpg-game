import pytest
from src.quest import Quest, QuestManager

def test_quest_creation():
    """Test that a quest can be created with required attributes"""
    quest = Quest(
        "Defeat the Dragon",
        "Slay the dragon terrorizing the village",
        ["Kill 5 enemies", "Collect dragon scales"],
        reward={"gold": 100, "experience": 50}
    )
    assert quest.title == "Defeat the Dragon"
    assert quest.description == "Slay the dragon terrorizing the village"
    assert len(quest.objectives) == 2
    assert quest.reward["gold"] == 100

def test_quest_completion():
    """Test quest completion tracking"""
    quest = Quest(
        "Defeat the Dragon",
        "Slay the dragon terrorizing the village",
        ["Kill 5 enemies", "Collect dragon scales"],
        reward={"gold": 100, "experience": 50}
    )
    assert not quest.is_completed()
    quest.complete_objective("Kill 5 enemies")
    assert not quest.is_completed()
    quest.complete_objective("Collect dragon scales")
    assert quest.is_completed()

def test_quest_manager():
    """Test quest management functionality"""
    manager = QuestManager()
    quest = Quest(
        "Defeat the Dragon",
        "Slay the dragon terrorizing the village",
        ["Kill 5 enemies"],
        reward={"gold": 100}
    )
    manager.add_quest(quest)
    assert len(manager.active_quests) == 1
    assert manager.get_quest("Defeat the Dragon") == quest

def test_quest_progress():
    """Test quest progress tracking"""
    quest = Quest(
        "Defeat the Dragon",
        "Slay the dragon terrorizing the village",
        ["Kill 5 enemies", "Collect dragon scales"],
        reward={"gold": 100}
    )
    assert quest.progress == 0
    quest.complete_objective("Kill 5 enemies")
    assert quest.progress == 50
    quest.complete_objective("Collect dragon scales")
    assert quest.progress == 100

def test_quest_rewards():
    """Test quest reward distribution"""
    quest = Quest(
        "Defeat the Dragon",
        "Slay the dragon terrorizing the village",
        ["Kill 5 enemies"],
        reward={"gold": 100, "item": "Dragon Scale"}
    )
    assert not quest.rewards_claimed
    # Complete the quest by completing its objectives
    quest.complete_objective("Kill 5 enemies")
    assert quest.is_completed()
    rewards = quest.claim_rewards()
    assert rewards == {"gold": 100, "item": "Dragon Scale"}
    assert quest.rewards_claimed
