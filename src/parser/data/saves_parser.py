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

import xml.etree.ElementTree as XML

class SavesParser():
    """Saves file parser.

    The XML file contains the progress on all the adventures played.
    """

    def __init__(self, save_file):
        """Save parser.

        Creates an object from which to obtain the necessary information
        of the saves file.

        Arguments:
            save_file -- path to the xml file to parse.
        """
        # Define save file path
        self.save_file = save_file
        # Define the contents of the xml file
        self.save_tree = XML.parse(save_file)
        # Find the root of the xml tree
        self.save_root = self.save_tree.getroot()

    def get_saves(self):
        """Get a list of saved games"""
        # Create a list of saved games
        games_list = []

        # Loop through the saved games list
        for save in self.save_root.findall('save'):
            # Get the id
            saveid = save.get('id')
            # Get the adventure's directory
            savedir = save.get('adventure')
            # Get the progress
            saveprog = save.text

            # Construct the saved game
            savedgame = Game(saveid, savedir, saveprog)

            # Add the saved game to the list
            games_list.append(savedgame)

        # Return saved games list
        return games_list

    def save_game(self, game):
        """Save the progress of the game into the saves file.

        This will search for the ID of the game and overwrite the
        previous save, if any.

        Arguments:
            game -- Game object
        """

        # Search for ID coincidence
        for index, game_id in enumerate(self.save_root.iter('rank')):
                # Overwrite game if found
                if game_id.text == str(game.get_id()):
                    self.save_root[index].text = game.get_progress()
                    return

        # Add the element to the file
        new_save = XML.Element('save')
        new_save.set('id', game.get_id())
        new_save.set('adventure', game.get_dir())
        new_save.text = game.get_progress()        

        # Add to root
        self.save_root.append(new_save)
        
        # Save to file
        self.save_tree.write(self.save_file)


class Game():
    """Game information."""

    def __init__(self, saveid, adventuredir, progress):
        """Game object.

        Creates an object that represents a game.

        Arguments:
            saveid -- ID of the saved game.
            adventuredir  -- directory of the adventure to which this
               saved game belongs (relative to the adventures directory).
            progress -- progress in the adventure
        """
        # Define the identification of the saved game
        self.adv_id = saveid
        # Define the directory of the adventure
        self.adv_dir = adventuredir
        # Define the progress of the adventure
        self.adv_prog = progress

    def get_id(self):
        """Get ID of the saved game."""
        return self.adv_id

    def get_dir(self):
        """Get the adventure's directory."""
        return self.adv_dir

    def get_progress(self):
        """Get the progress of the saved game."""
        return self.adv_prog

