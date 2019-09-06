# io_mesh_bls
Blockland Save (.bls) importer

Originally made by siba, updated for 2.8 by Ahead

![thing](https://i.imgur.com/7Sh2kD0.png)

## Instructions

* [Download the add-on](https://github.com/Ahe4d/io_mesh_bls/archive/master.zip) and install it in Edit > Preferences > Add-Ons
* Set your Blockland directory in the add-on drop-down config
* Copy the BLS_Bricks folder from the .zip into the **root** of your Blockland folder you specified in the config
* Find your save file in the open dialog, open
* ???
* Profit

## Issues

* `cannot read byte 0xb0 (or whatever)`: Your save file is encoded with a format that isn't UTF-8, the importer has problems reading brick files with special characters. (ex. bricks with a degree symbol) Make a copy of your save with UTF-8 encoding and try again.
* Importer takes too long: The importer has problems reading saves with a lot of bricks, please either try the Join Brick Meshes option or cut your builds down to small sizes or into separate files.
* `cannot find blb`: You're most likely missing a brick file that is referenced in the save file (& your Blockland directory in the config). Unfortunately since Blockland saves store bricks with their UI name, it is a hassle to track down the appropriate brick and rename it accordingly (ESPECIALLY with non-default bricks, but they will work in the importer), so you're going to have to rename a bunch of bricks if you're willing to go that route. (to do: make a script that creates a set of brick files with their internal and UI names)
* `cannot find something like brickTOP.png`: Make sure you have set up the config for your Blockland directory in the add-on drop down. Otherwise the importer won't work!
* Brick textures are stretched or look wrong: This is because I forgot to set up the texture nodes properly with a coordinates node. Will be added in a later update.
