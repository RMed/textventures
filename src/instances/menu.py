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

from parser.adventure import meta_parser as pmeta
from parser.adventure import scenario_parser as pscenario
from parser.data import saves_parser as psaves
from key_navigation import Listener, Action
from game import Game

import xml.etree.ElementTree as XML
import sys, os

# Configuration directory
CONF_DIR = os.path.join(os.path.expanduser('~'), '.textventures')

def clear_screen():
    """Clear the screen when navigating the menu."""

    # Check platform
    if sys.platform.startswith('win'):
        # Windows
        os.system('cls')
    else:
        # UNIX
        os.system('clear')

def main_menu():
    """Display the main menu.

    This function must check what keys have been pressed by the player
    for navigation purposes
    """

    # Clear screen
    clear_screen()

    # Check if the configuration directory exists
    if not os.path.isdir(CONF_DIR):
        # Create the directory tree
        try:
            os.mkdir(CONF_DIR)
            os.mkdir(os.path.join(CONF_DIR, 'adventures'))
            os.mkdir(os.path.join(CONF_DIR, 'adventures', 'stories'))
        except:
            print 'Could not create configuration directory'

    # Print program information
    print 'TextVentures - Main Menu\n'

    # Print navigation menu
    print '(N)ew game'
    print '(L)oad game'
    print '(E)xit'

    # Wait for user input
    while True:
        # Key listener
        key_listener = Listener()
        key = key_listener()
        # Action parser
        action_parser = Action(key, 'main')
        action = action_parser()

def load_menu():
    """Display the load game menu.

    Opens the saves file (if any) and shows all the games saved.
    The player must write the number of the game to load.
    """

    # Clear screen
    clear_screen()

    # Print information
    print 'TextVentures - Load Game\n'
    print '(C)hoose game to load'
    print '(B)ack\n'

    # Saves list
    saves_list = []

    # Check if the saves file exists
    saves_file = os.path.join(CONF_DIR, 'adventures', 'saves.xml')
    if os.path.isfile(saves_file):
        # Parse the file
        saves_parser = psaves.SavesParser(saves_file)
        # Fill the list
        saves_list = saves_parser.get_saves()
    else:
        try:
            # Need to create the file
            saves_tag = XML.Element('savefile')
            saves_tree = XML.ElementTree(saves_tag)
            saves_tree.write(saves_file)
        except:
            print 'Could not create the saves file'

    # Print the saves (if any)
    if not saves_list:
        # No saved games
        print 'There are no saved games'
    else:
        # Print games
        for index, save in enumerate(saves_list):
            print str(index) + ')'
            print 'ID: ' + save.get_id()
            print 'Adventure: ' + save.get_dir()
            print 'Progress: ' + save.get_progress()
            print '--------------'

    # Wait for user input
    while True:
        # Key listener
        key_listener = Listener()
        key = key_listener()
        # Action Parser
        action_parser = Action(key, 'load')
        action = action_parser()

def newgame_menu():
    """Display the new game menu.
    
    Show a list of available adventures and relevant information.
    """

    # Clear screen
    clear_screen()

    # Print information
    print 'TextVentures - New game\n'
    print '(C)hoose adventure'
    print '(B)ack\n'

    # Adventure list
    adventure_list = []

    # Get adventures
    adventure_parser = pmeta.AdventureParser(CONF_DIR)
    adventure_list = adventure_parser.get_adventures()

    # Print adventures
    if not adventure_list:
        print 'No adventures available'
    else:
        for index, adventure in enumerate(adventure_list):
            print str(index) + ')'
            print 'Title: ' + str(adventure.get_title())
            print 'Description: ' + str(adventure.get_description())
            print 'Author: ' + str(adventure.get_author())
            print 'Email: ' + str(adventure.get_email())
            print 'URL: ' + str(adventure.get_url())
            print 'Version: ' + str(adventure.get_version())
            print '-----------------'

    # Wait for user input
    while True:
        # Key listener
        key_listener = Listener()
        key = key_listener()
        # Action parser
        action_parser = Action(key, 'new')
        action = action_parser()
        
        if not action == 'c':
            continue

        # Ask for the game to load
        input_num = raw_input('Please write an adventure number to load: ')
        # Check if int
        try:
            game_index = int(input_num)
            # Check if out of bounds
            if game_index >= len(adventure_list):
                print 'Please write a valid number'
                continue
        except:
            print 'Please write a valid number'
            continue

        # Get directory
        adventure_dir = adventure_list[game_index].get_location()

        # Ask for an ID for the game
        input_id = raw_input('Please write an ID for this adventure: ')

        # Get the first scenario
        first = adventure_list[game_index].get_first()

        # Build game
        new_game = psaves.Game(input_id, adventure_dir, first)

        # Load the game
        start_game = Game(new_game, CONF_DIR)
        game = start_game()


