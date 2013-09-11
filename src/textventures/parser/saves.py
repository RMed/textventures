# -*- coding: utf-8 -*-
# This file is part of TextVentures - https://github.com/RMed/textventures
#
# Copyright (C) 2013 Rafael Medina García <rafamedgar@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import config

import xml.etree.ElementTree as XML
import os

def get_saves():
    """Get a list of saved games in the saves file."""
    # Create a list of saved games
    games_list = []

    # Parse file
    save_tree = XML.parse(config.SAVES_FILE)
    save_root = save_tree.getroot()

    # Loop through the saved games list
    for save in save_root.findall('save'):
        # Get the id
        saveid = save.get('id')
        # Get the adventure's directory
        savedir = save.get('adventure')
        # Get the progress
        saveprog = save.get('progress')
        # Get scenario title        
        savetitle = save.text

        # Construct the saved game
        savedgame = Game(saveid, savedir, saveprog, savetitle)

        # Add the saved game to the list
        games_list.append(savedgame)

    # Return saved games list
    return games_list

def save_game(game):
    """Save the progress of the game into the saves file.

    This will search for the ID of the game and overwrite the
    previous save, if any.

    Arguments:
        game -- Game object
    """
    # Check if the saves file exists
    if not os.path.isfile(config.SAVES_FILE):
        try:
            # Need to create the file
            saves_tag = XML.Element('savefile')
            saves_tree = XML.ElementTree(saves_tag)
            saves_tree.write(config.SAVES_FILE)
        except:
            print 'Could not create the saves file'

    # Parse file
    save_tree = XML.parse(config.SAVES_FILE)
    save_root = save_tree.getroot()

    # Fill the list
    saves_list = get_saves()

    # Search for ID coincidence
    print game.get_id()
    for index, saved_game in enumerate(save_root):
            # Overwrite game if found
            if (saved_game.get('id') == game.get_id()) and \
                    (saved_game.get('adventure') == game.get_dir()):

                save_root[index].set('progress', game.get_progress())
                save_root[index].text = game.get_title()
                save_tree.write(config.SAVES_FILE)
                return

    # Add the element to the file
    new_save = XML.Element('save')
    new_save.set('id', game.get_id())
    new_save.set('adventure', game.get_dir())
    new_save.set('progress', game.get_progress())
    new_save.text = game.get_title()        

    # Add to root
    save_root.append(new_save)
        
    # Save to file
    save_tree.write(config.SAVES_FILE)


class Game():
    """Game information."""

    def __init__(self, saveid, adventuredir, progress, title="None"):
        """Game object.

        Creates an object that represents a game.

        Arguments:
            saveid -- ID of the saved game.
            adventuredir  -- directory of the adventure to which this
               saved game belongs (relative to the adventures directory).
            progress -- progress in the adventure
            title -- title of the current scenario
        """
        # Define the identification of the saved game
        self.adv_id = saveid
        # Define the directory of the adventure
        self.adv_dir = adventuredir
        # Define the progress of the adventure
        self.adv_prog = progress
        # Define the title of the scenario
        self.adv_title = title

    def get_id(self):
        """Get ID of the saved game."""
        return self.adv_id

    def get_dir(self):
        """Get the adventure's directory."""
        return self.adv_dir

    def get_progress(self):
        """Get the progress of the saved game."""
        return self.adv_prog

    def set_progress(self, new_progress):
        """Update the progress of the saved game."""
        self.adv_prog = new_progress

    def get_title(self):
        """Get the title of the saved game."""
        return self.adv_title

    def set_title(self, new_title):
        """Update the title of the saved game."""
        self.adv_title = new_title

