# io-mesh-bls
Blockland save importer

Originally made by siba, updated for 2.8 by Ahead

![thing](https://i.imgur.com/7Sh2kD0.png)

## Instructions

* [Download the add-on](https://github.com/Ahe4d/io-mesh-bls/archive/master.zip)
* Install the add-on
* Copy the BLS_Bricks folder from the .zip into the **root** of your Blockland folder.
* Find your save file in the open dialog, open
* ???
* Profit

## Issues

* `cannot read byte 0xb0 (or whatever)`: Your save file is encoded with a format that isn't UTF-8, the importer has problems reading brick files with special characters. (ex. bricks with a degree symbol) Make a copy of your save with UTF-8 encoding and try again.
* Importer takes too long: The importer has problems reading saves with a lot of bricks (blame Blender?? maybe add option to join all bricks), please cut your builds down to small sizes or into separate files.
* `cannot find blb`: You're most likely missing a brick file that is referenced in the save file. Unfortunately since Blockland saves store bricks with their UI name, it is a hassle to track down the appropriate brick and rename it accordingly (ESPECIALLY with non-default bricks, but they will work in the importer), so you're going to have to rename a bunch of bricks if you're willing to go that route. (to do: make a script that creates a set of brick files with their internal and UI names)
* `cannot find something like brickTOP.png`: Make sure your Blockland directory is in your Documents folder of the current user. Otherwise the importer won't work! (I will add a config soon)
* Brick textures are stretched or look wrong: This is because I forgot to set up the texture nodes properly with a coordinates node. Will be added in a later update.
