import random

class Character:
    def __init__(self, name, attacks):
        self.name = name
        self.attacks = attacks

class Battle:
    def __init__(self, character):
        self.character = character
        self.enemy_hp = random.randint(100, 1000)

    def attack(self, attack_index):
        attack = self.character.attacks[attack_index]
        self.enemy_hp -= attack["damage"]
        return attack["name"], attack["damage"], self.enemy_hp

    def is_enemy_defeated(self):
        return self.enemy_hp <= 0

# Character classes
CHARACTER_CLASSES = [
    Character("Hunter", [
        {"name": "Arrow Shot", "damage": 50},
        {"name": "Multi Arrow", "damage": 30},
        {"name": "Poison Arrow", "damage": 40},
        {"name": "Precision Shot", "damage": 70}
    ]),
    Character("Mage", [
        {"name": "Fireball", "damage": 60},
        {"name": "Ice Spike", "damage": 45},
        {"name": "Lightning Bolt", "damage": 55},
        {"name": "Arcane Blast", "damage": 80}
    ]),
    Character("Beast Tamer", [
        {"name": "Wolf Bite", "damage": 40},
        {"name": "Eagle Strike", "damage": 35},
        {"name": "Bear Claw", "damage": 50},
        {"name": "Pack Attack", "damage": 65}
    ]),
    Character("Tank", [
        {"name": "Shield Bash", "damage": 30},
        {"name": "Heavy Strike", "damage": 45},
        {"name": "Ground Slam", "damage": 40},
        {"name": "Berserker Rage", "damage": 60}
    ])
] 