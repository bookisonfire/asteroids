[boot.dev](https://www.boot.dev) asteroids project

![image](https://github.com/user-attachments/assets/b3919632-d144-4dd4-8b9a-a46cf0e92dcc)


Ideas to extend the project in the future. 


    ✅ Add a "game over" screen
    ✅ Add a scoring system
    ✅ Implement multiple lives and respawning
    ✅ Add an explosion effect for the asteroids
    Add acceleration to the player movement
    ✅ Make the objects wrap around the screen instead of disappearing
    ✅ Add a background image
    Create different weapon types
    ✅ Make the asteroids lumpy instead of perfectly round
    ✅ Make the ship have a triangular hit box instead of a circular one
    Add a shield power-up
    Add a life power-up
    ✅ Add a main menu
    ✅ Add a pause menu


Be sure to post your highscores!
And feel free to dm any requests or new ideas 
💜 [David B](linktr.ee/bookisonfire)

---

## How to Install and Run the Game

### 1. Install Python (Recommended: Python 3.7–3.9 for best compatibility)
- Download from https://www.python.org/downloads/
- On Windows, check "Add Python to PATH" during install.

### 2. Install Requirements
Open a terminal or command prompt in this folder and run:

```
pip install -r requirements.txt
```

### 3. Run the Game

```
python main.py
```

### 4. (Optional) Build a Standalone Executable (Windows)
- Install PyInstaller:
  ```
  pip install pyinstaller
  ```
- Build the executable:
  ```
  pyinstaller --onefile --add-data "assets;assets" main.py
  ```
- The executable will be in the `dist/` folder.

### Notes for Windows 7
- Use Python 3.7, 3.8, or 3.9 (not 3.10+).
- Use Pygame 2.x.
- If you see errors, try building and running on a Windows 7 machine or VM.

---


