import pytest
from fastapi.testclient import TestClient
from src.main import app, CHARACTER_CLASSES
import pygame

client = TestClient(app)

def test_home_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "Hunter" in response.text
    assert "Mage" in response.text
    assert "Beast Tamer" in response.text
    assert "Tank" in response.text

def test_character_classes():
    response = client.get("/")
    assert response.status_code == 200
    content = response.text
    # Check if all character classes are present
    assert "Expert in ranged combat and tracking" in content  # Hunter
    assert "Master of arcane arts and spells" in content     # Mage
    assert "Controls and commands wild creatures" in content # Beast Tamer
    assert "Heavy armor and defensive specialist" in content # Tank 

def test_character_classes_exist():
    assert len(CHARACTER_CLASSES) == 4
    assert any(c["name"] == "Hunter" for c in CHARACTER_CLASSES)
    assert any(c["name"] == "Mage" for c in CHARACTER_CLASSES)
    assert any(c["name"] == "Beast Tamer" for c in CHARACTER_CLASSES)
    assert any(c["name"] == "Tank" for c in CHARACTER_CLASSES)

def test_character_class_properties():
    for char_class in CHARACTER_CLASSES:
        assert "name" in char_class
        assert "description" in char_class
        assert "rect" in char_class
        assert isinstance(char_class["rect"], pygame.Rect) 