# Crystalled Bullets Dialogue Manager

A Dialogue Manager intented to be used in Crystalled Bullets.
Written in PyQt6.

# Screenshots

![Screenshots](screenshots/スクリーンショット_20260321_161949.png) 
![Screenshots](screenshots/in-game-shot.webp) 

## Features

- Generates appopriate ZScript depends on voice line's seconds length.
- Small Text Editor jointed on bottom.
- Skippable Text by Jump Button.
- Generates blink animation (optional, only if entered blink animation frame.)
- Generates Lip Sync Animation (again, optional. only if you entered open mouth animation)

## ToDo

- Support for automatic assign on lipsync which audio file user loaded.
- GUI Editor for "TNT1 A 0 CB_SpeakDialogue"

## Contributing

Contributions are welcome! If you have ideas or improvements, feel free to fork the repo and submit a pull request. For major changes, please open an issue first to discuss what you'd like to change.

## Tech Stacks
- Python (obviously)
- PyQt6
- Mutagen

If you want run this application on your system, please install the required dependency on pip or your Linux package manager, such as pacman or AUR.
Currently, only Linux is supported. And I have no idea how to run it on Windows machines.

## Licences

Licence of this very own program(Python) is **GPL3** Licenced. Thus, please follow GPL3's basic rules of copyleft when you're redistribute or modify it. 
However, the dialgoue code(ZScript) generated with this program is belong to yours. Feel free to use it to your Crystalled Bullets mod, as well as Doom mods or commercial ZDoom game for your needs.
