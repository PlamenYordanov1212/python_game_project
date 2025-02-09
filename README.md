# Ascension

Ascension is a 2D auto-scroll game made using **Python** and the **Pygame** library for the FMI Sofia course "Programming with Python".

## Installation
1. Clone the repository

```bash
git clone https://github.com/PlamenYordanov1212/python_game_project
cd python_game_project
```

2. Create a virtual environment(Windows)

```
python -m venv venv
```

3. Activate the virtual environment(Windows)

```
venv\Scripts\activate
```

4. Install packages

```
pip isntall -r requirements.txt
```
5. Start the game

```
python main.py
```


## Premise and Controls

The objective of the game is to **destroy orbs** in order to fill a **constantly depleting energy bar**. The game ends **unsuccsessfully** if the bar is depleted or **successfully** if the bar is completely filled. Best time for completion is also tracked with a timer.

### Phase One
The player character automatically runs while orbs spawn at a random height. Once the bar is filled to about 50%, the character transforms, starts flying and the second phase begins.

- A - move left
- D - move right
- Space - jump
- Left Mouse Button - attack (be sure to be close to the orbs when attacking in order to destroy them)

### Phase Two

The player character has transformed into a more powerful form and can now fly. He only needs to clash into the orbs in order to destroy them. The orbs themselves move faster and fireballs start spawning which deplete the energy bar, if they hit the player character.

- W - fly up
- A - fly left
- S - fly down
- D - fly right

## External Asset References
- [Music and sound effects](https://pixabay.com/sound-effects/)
- [Player character first phase](https://craftpix.net/freebies/free-pixel-art-tiny-hero-sprites/)
- [Player character second phase](https://www.spriters-resource.com/game_boy_advance/sonicadv3/sheet/7150/)
- [Background second phase](https://www.peakpx.com/en/hd-wallpaper-desktop-eigib)
- [Fireball](https://opengameart.org/content/fireball-spell)
- [Orb](https://www.pngegg.com/en/png-fpzgt)