# Flux Neutral Coil Generator

Big thanks to [Starfish Neuroscience](https://starfishneuroscience.com/) for sponsoring this work and allowing me to share it!

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

1. Launch by opening KiCAD -> Footprint Editor -> Footprint Wizard (second icon, the one with the red star)
1. If it was installed correctly, it should show up at the end of the list of footprint wizards.
1. Select and click OK. 
1. Adjust the parameters as needed.  Please note the limitations below, especially the inner layers not showing up in preview.
1. Export the footprint to the editor. (Last icon in the upper left.)
1. Save this to an appropriate footprint library.  
1. Add the Net Tie.  NOTE: This step is mandatory for the DRC to come out clean.  It should be done automatically, but it's a limitation of KiCAD. 
    1. Open the Footprint Properties by using the menu File -> Footprint Properties.
    1. Select the Clearance Overrides and Settings tab.
    1. In the Net Ties section at the bottom, add an entry of "1,2,3"
    1. Click OK and save the footprint. 
1. From here, just use this as a footprint for an inductor in KiCAD, as it follows the normal design flow.

Note: the "why" you'd want a flux-neutral coil is kinda up to you.  

## Limitations

This tool will have several limitations in it's current state.

1. It will not check for manufacturability of the coil.  However, you can do this in PCBNew.
1. It will not check all conditions of if it will make a shape that's not plausible.  Specifically, using a min-radius of 0 will cause issues with the vias. 
1. At it's current setup, it will only generate a 2 layer configuration. Using more than 2 layers will probably need a different topology.
1. The footprint needs to have a Net Tie added after it's exported out of the Wizard.  This will prevent the DRC errors.
1. If setting the layers to an inner layer, the Footprint Wizard will not display correctly.  This is a bug/limitation of KiCAD.  Once it's exported, it will work correctly.  One alternative to this is to generate the shape with F_Cu/B_Cu, and then do a text replacement after the fact.

## To dos!

1. TODO: Fix the sign of the various variables. It feels like often the +/- is counter intuitive within the calculations.
1. TODO: Figure out how to programmatically add a Net Tie
