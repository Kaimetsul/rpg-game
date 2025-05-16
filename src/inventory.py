class Item:
    """Represents an item in the game inventory"""
    def __init__(self, name, type, value):
        self.name = name
        self.type = type
        self.value = value

class Inventory:
    """Manages the player's inventory of items"""
    def __init__(self, items=None, max_size=20):
        self.items = items or []
        self.max_size = max_size

    def add_item(self, item):
        """Add an item to the inventory if there's space"""
        if len(self.items) >= self.max_size:
            raise ValueError("Inventory is full")
        self.items.append(item)

    def remove_item(self, item_name):
        """Remove and return an item from the inventory by name"""
        for i, item in enumerate(self.items):
            if item.name == item_name:
                return self.items.pop(i)
        raise ValueError(f"Item {item_name} not found in inventory")

    def get_item(self, item_name):
        """Get an item from the inventory by name without removing it"""
        for item in self.items:
            if item.name == item_name:
                return item
        raise ValueError(f"Item {item_name} not found in inventory")

    def is_full(self):
        """Check if the inventory is full"""
        return len(self.items) >= self.max_size

    def get_items_by_type(self, type):
        """Get all items of a specific type"""
        return [item for item in self.items if item.type == type]
