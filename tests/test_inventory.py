import pytest
from src.inventory import Inventory, Item

def test_inventory_creation():
    """Test that an inventory can be created with initial items"""
    items = [
        Item("Health Potion", "Consumable", 10),
        Item("Sword", "Weapon", 20)
    ]
    inventory = Inventory(items)
    assert len(inventory.items) == 2
    assert inventory.items[0].name == "Health Potion"
    assert inventory.items[1].name == "Sword"

def test_add_item():
    """Test adding an item to inventory"""
    inventory = Inventory([])
    item = Item("Health Potion", "Consumable", 10)
    inventory.add_item(item)
    assert len(inventory.items) == 1
    assert inventory.items[0].name == "Health Potion"

def test_remove_item():
    """Test removing an item from inventory"""
    item = Item("Health Potion", "Consumable", 10)
    inventory = Inventory([item])
    removed = inventory.remove_item("Health Potion")
    assert removed.name == "Health Potion"
    assert len(inventory.items) == 0

def test_get_item():
    """Test retrieving an item from inventory"""
    item = Item("Health Potion", "Consumable", 10)
    inventory = Inventory([item])
    found = inventory.get_item("Health Potion")
    assert found.name == "Health Potion"
    assert found.type == "Consumable"
    assert found.value == 10

def test_inventory_full():
    """Test inventory capacity limits"""
    inventory = Inventory([], max_size=2)
    inventory.add_item(Item("Health Potion", "Consumable", 10))
    inventory.add_item(Item("Sword", "Weapon", 20))
    with pytest.raises(ValueError):
        inventory.add_item(Item("Shield", "Armor", 15))
