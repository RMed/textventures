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

            # Construct the saved game
            savedgame = SavedGame(saveid, savedir)

            # Add the saved game to the list
            games_list.append(savedgame)

        # Return saved games list
        return games_list

class SavedGame():
    """Saved game information retreived from the XML file."""

    def __init__(self, saveid, adventuredir):
        """SavedGame object.

        Creates an object that represents a saved game.

        Arguments:
            saveid -- ID of the saved game.
            savedir -- Directory of the adventure to which this saved
                   game belongs (relative to the adventures directory).
        """
        # Define the identification of the saved game
        self.id = saveid
        # Define the directory of the adventure
        self.advdir = adventuredir

    def get_id(self):
        """Get ID of the saved game."""
        return self.id

    def get_dir(self):
        """Get the adventure's directory."""
        return self.advdir

