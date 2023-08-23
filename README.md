# Flux Neutral Coil Generator

Big thanks to Starfish Neuro for sponsoring this work and allowing me to share it!

## Background

There is a need to generate flux-neutral coils that can take up the largest area
within a space.  In the case of Starfish Neuro, that was a circular aperture.  
This tool was developed to quickly iterate on various coil parameters without
having to re-draw things by hand.

## Installation

This tool is intended to be used within the KiCAD Footprint Wizard tool. To do
so requires "installation" into KiCAD.  This is either placing this whole repo
within the appropriate directory, or placing a shortcut or symbolic link in that
directory.

This tool has been tested with KiCAD 7.0.7.  It might work with other versions
(6.x and 7.0.x), but has not been tested. 

### For Linux:
1. Clone the Repo into `~/.local/share/kicad/7.0/scripting/plugins/`

OR 

(Needs to be tested for accuracy, but this is the method I'm using)
1. Clone the repo into your preferred location.
2. `cd flux-neutral-coil-generator`
3. `ln -s ${PWD}/flux_neutral_coil_generator.py ~/.local/share/kicad/7.0/scripting/plugins/flux_neutral_coil_generator.py`

### For Mac

TODO but should be similar to Linux

### For Windows

TODO but should be maybe-sorta similar to Linux

## Usage

TODO!

## Limitations

This tool will have several limitations in it's current state.

1. It will not check for manufacturability of the coil
1. It will not check all conditions of if it will make a shape that's not plausible.
1. At it's current setup, it will only generate a 2 layer configuration. 

## To dos!

1. TODO: Account for trace thickness in gap creation.  