# RPG Game with CI/CD Pipeline

A Python-based RPG game with a complete CI/CD pipeline using Jenkins and Docker.

## Features

- Character selection with unique abilities
- Battle system with multiple attacks
- Maze navigation
- Inventory system
- Quest system
- Save/Load game state

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/Kaimetsul/rpg-game.git
cd rpg-game
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the game:
```bash
python src/main.py
```

## Testing

Run tests with:
```bash
pytest tests/
```

Run tests with coverage:
```bash
pytest tests/ --cov=src --cov-report=term-missing
```

## CI/CD Pipeline

The project uses Jenkins for continuous integration and deployment:

1. **Build Stage**: Creates a Docker container with the game
2. **Test Stage**: Runs unit tests with coverage reporting
3. **Code Quality Stage**: Runs flake8 and pylint for code quality checks
4. **Deploy Stage**: Prepares the game for deployment

## Project Structure

```
rpg-game/
├── src/
│   ├── main.py          # Main game loop
│   ├── game.py          # Game mechanics
│   ├── ui.py            # User interface
│   ├── inventory.py     # Inventory system
│   └── quest.py         # Quest system
├── tests/
│   ├── test_game.py
│   ├── test_ui.py
│   ├── test_inventory.py
│   └── test_quest.py
├── Dockerfile
├── Jenkinsfile
└── requirements.txt
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Write tests for new features
4. Submit a pull request

## License

This project is licensed under the MIT License.
