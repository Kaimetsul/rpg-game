import unittest
from src.game import Character, Battle

class TestGame(unittest.TestCase):
    def test_character_selection(self):
        character = Character("Hunter", [{"name": "Arrow Shot", "damage": 50}])
        self.assertEqual(character.name, "Hunter")
        self.assertEqual(character.attacks[0]["name"], "Arrow Shot")
        self.assertEqual(character.attacks[0]["damage"], 50)

    def test_attack_damage(self):
        character = Character("Mage", [{"name": "Fireball", "damage": 60}])
        battle = Battle(character)
        attack_name, damage, enemy_hp = battle.attack(0)
        self.assertEqual(attack_name, "Fireball")
        self.assertEqual(damage, 60)
        self.assertGreaterEqual(enemy_hp, 100)
        self.assertLessEqual(enemy_hp, 1000)

    def test_battle_mechanics(self):
        character = Character("Tank", [{"name": "Shield Bash", "damage": 30}])
        battle = Battle(character)
        battle.enemy_hp = 30
        self.assertFalse(battle.is_enemy_defeated())
        battle.attack(0)
        self.assertTrue(battle.is_enemy_defeated())

if __name__ == "__main__":
    unittest.main() 