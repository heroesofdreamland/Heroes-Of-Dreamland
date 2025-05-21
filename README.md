# Heroes of Dreamland

Welcome to **Heroes of Dreamland**, my first open-source game project with an engine entirely built in Python! Create your dream game without bureaucracy, job hunting, or stress—just pure fun and a place where everyone can contribute.

## Project Journey
It all started small with **Heroes of Dreamland v1.0**.  
*Video placeholder*

Six months later, I proudly present **Heroes of Dreamland v2.0**!  
*Video placeholder*

## Current Achievements
The project has reached significant milestones:
- **Clean architecture**: Well-structured and maintainable codebase.
- **Physics and AI**: Fully developed physics engine and unit intelligence.
- **Graphics Engine**: Built using OpenGL for rendering.
- **UI Layout Engine**: Robust system for designing user interfaces.
- **Isometric Map Generation**: Engine for creating isometric game maps.
- **Unit and Projectile Lifecycle**: Comprehensive systems for units and projectiles.
- **Level and Progression System**: Leveling and level-up mechanics.
- **Unit Mechanics**:
  - Respawn
  - Trojan (enemies spawn smaller enemies upon death)
  - Unit summoning during combat
  - Currency consumption
  - Explosion
  - Status effects (poison, freeze, stun)
  - Ranged and melee combat
  - Cowardly enemies (flee when approached)
- **Event System**: Handles in-game events like enemy/player death, inventory state, etc.
- **Settings**: Includes debug mode, screen resolution, and keybinding customization.
- **Progress Saving**: Saves game progress and settings.
- **Quest System**: Fully functional quest mechanics.
- **Hero Selection**: Choose your hero.
- **Item Vendor**: Trade items with an in-game merchant.
- **Items and Summons**: Extensive item and summon systems.
- **And more!** The project currently includes:
  - Over 200 Python files for game logic.
  - 600+ unit models (sourced from the open-source project [open-duelyst/duelyst](https://github.com/open-duelyst/duelyst)).
  - 80+ item models and 100+ effect models.

**Performance**: The game runs smoothly at 100–120 FPS with 40–60 units on the map—a major achievement for me!

## Create Your Dream Game
Build new units, name them as you like, create new mechanics or use existing ones, design quests, and craft new maps! Your contributions matter, and you can start right now. Most importantly, enjoy the process!

Check my project's Trello board (linked in the repository) for task ideas if you're unsure where to start.

## Why Open Source?
When I started *Heroes of Dreamland*, my goal was to create not just a game but a platform for developers, driven by the community. I want this project to be a place where everyone—from beginners to seasoned game developers—can:
- Learn core game development concepts on a real project.
- Build a dream game you'd love to play.
- Explore and enhance a new game engine.
- Experiment wildly in the *chaos* branch (more on that below).
- Find a team, connect with like-minded people, or just have fun with friends.

This project will **never be commercial**. There are **no deadlines**—just pure enjoyment!

## Game Genre
Initially designed as a roguelike or dungeon runner, *Heroes of Dreamland* is now at a stage where the community can shape its direction. With my current engine, it can pivot to a roguelike, a Diablo-like ARPG, a MOBA prototype, or even an RPG. The stable version is my starting point, and I’ll decide the path together with the community as the project progresses.

*Note*: Multiplayer is not planned at this stage; the game is single-player only.

## How to Play
Currently, you can build and run the project locally via GitHub. I’m planning a website with downloadable pre-built versions in the near future, making it accessible to everyone.

### Setup Instructions
To run the project, you need **Python 3.12**. Follow these steps:

1. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   ```
   Or, if `python3` is required (common on Linux/macOS):
   ```bash
   python3 -m venv venv
   ```

2. **Activate the virtual environment**:
   ```bash
   source venv/bin/activate  # Linux/macOS
   .\venv\Scripts\activate   # Windows
   ```

3. **Install dependencies** listed in `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
   Or, if `pip3` is required:
   ```bash
   pip3 install -r requirements.txt
   ```

4. **Run the game** by executing the main file:
   ```bash
   python game.py
   ```

### Project Structure
- **logic/**: Core game logic
  - **controller/**: Handles dynamic game logic for all systems.
  - **core/**: My game engine (physics, rendering, etc.). *Note*: Complex and not recommended for initial exploration.
  - **entities/**: Logic for all game entities.
    - **abilities/**: Unit abilities (movement, combat, explosions, etc.).
    - **effects/**: Logic for status effects.
    - **items/**: Item logic.
    - **orders/**: Quest logic (quests are called "orders" and issued by a green NPC).
    - **projectiles/**: Projectile logic.
    - **rewards/**: Rewards for quests, level-ups, and kills.
    - **units/**: Unit logic.
  - **environment/**: Complex environment logic (avoid for now).
  - **events/**: In-game event system (e.g., deaths, inventory changes).
  - **level_design/**: Scenes, level logic, and map generation.
  - **settings/**: Game settings (from the settings menu).
  - **ui/**: UI tools (fonts, colors, unit status bars).
- **utils/**: Utility tools, e.g., for slicing unit textures using `.plist` files.
- **resources/**: Game assets, saved data, and settings.

### Troubleshooting
- **Missing `game_data` folder**: If the `HoD/resources/game_data/` folder is missing, create it manually. This folder stores settings and progress (rare issue).
- **Incorrect resolution**: Go to *Settings > Screen* in-game to select your preferred resolution.
- **Box-camera issues**: If the camera behavior feels off, set the `box-camera` value to `0` in settings to make it follow the player.

If you encounter other issues, please report them to help improve my project!

## How the Community Can Help
1. **Contributions and Ideas**: Propose or code new features, modes, mechanics, quests, units, bosses, or bug fixes. All contributions are welcome via GitHub or community channels.
2. **Testing and Feedback**: Help identify bugs and issues. The more testers, the more stable and polished the game becomes.
3. **Design and Graphics**: Contribute improvements to design, animations, textures, or sprites to enhance the game’s visuals.
4. **Learning and Growth**: Perfect for beginners! Participate to learn game development, teamwork, and collaboration. I’m working on a learning program for new developers.

## Development Branches
My project uses three main branches:
- **main**: The stable branch moving toward an RPG-roguelike. Pull requests (PRs) must maintain performance, architecture, and avoid malicious code.
- **chaos**: A playground for all PRs (no malicious code allowed). Want an anime-style boss or performance-breaking features? This is the place! This branch showcases how unchecked features can harm a project. I periodically reset it from `main`, but old versions are preserved for fun.
- **modes**: Planned for future in-game modes, allowing custom games on my engine (details to come).

## Contributing
I welcome contributions of all kinds! To get started:
1. Fork the repository.
2. Create a branch for your feature or fix (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m "Add your feature"`).
4. Push to your branch (`git push origin feature/your-feature`).
5. Open a pull request to the appropriate branch (`main` or `chaos`).

Check my Trello board [Trello](https://trello.com/b/dRa1dr9j/heroes-of-dreamland) for task ideas or propose your own.

## Contact
Join my community on [Trello](https://trello.com/b/dRa1dr9j/heroes-of-dreamland) or [X.com](https://x.com/H_o_Dreamland) or raise issues/PRs on GitHub. Let’s build *Heroes of Dreamland* together!