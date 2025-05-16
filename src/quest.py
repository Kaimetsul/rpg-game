class Quest:
    """Represents a quest in the game"""
    def __init__(self, title, description, objectives, reward):
        self.title = title
        self.description = description
        self.objectives = {obj: False for obj in objectives}
        self.reward = reward
        self.rewards_claimed = False

    def complete_objective(self, objective):
        """Mark an objective as completed"""
        if objective in self.objectives:
            self.objectives[objective] = True
        else:
            raise ValueError(f"Objective {objective} not found in quest")

    def is_completed(self):
        """Check if all objectives are completed"""
        return all(self.objectives.values())

    @property
    def progress(self):
        """Calculate quest completion percentage"""
        if not self.objectives:
            return 0
        completed = sum(1 for completed in self.objectives.values() if completed)
        return (completed / len(self.objectives)) * 100

    def claim_rewards(self):
        """Claim quest rewards"""
        if not self.is_completed():
            raise ValueError("Cannot claim rewards before quest is completed")
        if self.rewards_claimed:
            raise ValueError("Rewards have already been claimed")
        self.rewards_claimed = True
        return self.reward

class QuestManager:
    """Manages all quests in the game"""
    def __init__(self):
        self.active_quests = {}
        self.completed_quests = {}

    def add_quest(self, quest):
        """Add a new quest to the active quests"""
        if quest.title in self.active_quests:
            raise ValueError(f"Quest {quest.title} already exists")
        self.active_quests[quest.title] = quest

    def get_quest(self, title):
        """Get a quest by title"""
        return self.active_quests.get(title)

    def complete_quest(self, title):
        """Mark a quest as completed and move it to completed quests"""
        if title not in self.active_quests:
            raise ValueError(f"Quest {title} not found")
        quest = self.active_quests.pop(title)
        self.completed_quests[title] = quest

    def get_active_quests(self):
        """Get all active quests"""
        return list(self.active_quests.values())

    def get_completed_quests(self):
        """Get all completed quests"""
        return list(self.completed_quests.values())
