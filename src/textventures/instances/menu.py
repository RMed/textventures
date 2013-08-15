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

from .. parser.adventure import metadata
from .. parser.data import saves
from .. import config
from key_navigation import Listener, Action
from play import Play

import xml.etree.ElementTree as XML
import sys, os

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
    if not os.path.isdir(config.textventures_dir):
        # Create the directory tree
        try:
            os.mkdir(config.textventures_dir)
            os.mkdir(os.path.join(config.textventures_dir, 'adventures'))
        except:
            print 'Could not create configuration directory'

    # Print program information
    print 'TextVentures - Main Menu\n'

    # Print navigation menu
    print '[N]ew game'
    print '[L]oad game\n'
    print '[H]elp'
    print '[A]bout'
    print '[E]xit'

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

    # Print header
    print 'TextVentures - Load Game\n'

    # Saves list
    saves_list = []

    # Check if the saves file exists
    if not os.path.isfile(config.saves_file):
        try:
            # Need to create the file
            saves_tag = XML.Element('savefile')
            saves_tree = XML.ElementTree(saves_tag)
            saves_tree.write(config.saves_file)
        except:
            print 'Could not create the saves file'

    # Fill the list
    saves_list = saves.get_saves()

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

    # Show actions
    print '\n[C]hoose game to load'
    print '[B]ack'

    # Wait for user input
    while True:
        # Key listener
        key_listener = Listener()
        key = key_listener()
        # Action Parser
        action_parser = Action(key, 'load')
        action = action_parser()

        if not action == 'c':
            continue

        # Ask for the game to load
        input_num = raw_input('Please write a game number to load: ')

        # Check if the player wants to leave
        if input_num == 'cancel':
            load_menu()

        # Check if int
        try:
            game_index = int(input_num)
            # Check if out of bounds
            if game_index >= len(saves_list):
                print 'Please write a valid number'
                continue
        except:
            print 'Please write a valid number'
            continue

        # Get ID
        adventure_id = saves_list[game_index].get_id()

        # Get directory
        adventure_dir = saves_list[game_index].get_dir()

        # Get the progress
        progress = saves_list[game_index].get_progress()

        # Build game
        loaded_game = saves.Game(adventure_id, adventure_dir, 
                progress)

        # Load the game
        start_game = Play(loaded_game)
        game = start_game()
        
def newgame_menu():
    """Display the new game menu.
    
    Show a list of available adventures and relevant information.
    """

    # Clear screen
    clear_screen()

    # Print header
    print 'TextVentures - New game\n'

    # Adventure list
    adventure_list = []

    # Get adventures
    adventure_list = metadata.get_adventures()

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

    # Show actions
    print '\n[C]hoose adventure to start'
    print '[B]ack'

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

        # Check if the player wants to leave
        if input_num == 'cancel':
            newgame_menu()

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
        new_game = saves.Game(input_id, adventure_dir, first)

        # Load the game
        start_game = Play(new_game)
        game = start_game()

def help_menu():
    """Display the help menu.
    
    Show how to navigate and play the adventures."""

    # Clear screen
    clear_screen()

    # Print header
    print 'TextVentures - Help\n'

    # Print menu navigation help
    print '--- MENU NAVIGATION ---'
    print "Navigating through TextVenture's menus is fairly simple: in the"
    print "different menus, you will see the available options in the form"
    print "'[B]ack' (which, in this case, will take you back to the main"
    print "menu). The character between the braces represents the key to"
    print "be pressed in order to perform that action.\n"

    # Print game choosing help
    print '--- CHOOSING A GAME ---'
    print "In the New Game and Load Game menus, you will be presented with"
    print "several games available to you. In order to play any of these"
    print "games, you must first press the specified character (usually"
    print "[C]) and then write the game number. If you enter this mode and"
    print "want to leave, simply write the word 'cancel' and you will"
    print "return to the menu mode.\n"

    # Print adventure help
    print '--- PLAYING ---'
    print "While playing, the menu navigation keys will not work. Instead,"
    print "you will be presented with the prompt '->' and you will have to"
    print "write the correct command in order to advance in the story."
    print "Note that there may be several commands for each scenario of"
    print "the adventure. If you want to leave the game, simply write the"
    print "word 'exit' and you will be back in the main menu."
    print "The game is saved every time a scenario is loaded, so you do"
    print "not need to worry about your progress being lost.\n"

    # Show actions
    print '[B]ack'

    # Wait for user input
    while True:
        # Key listener
        key_listener = Listener()
        key = key_listener()
        # Action parser
        action_parser = Action(key, 'help')
        action = action_parser()

def about_menu():
    """Display the About menu containing program information."""

    # Clear screen
    clear_screen()

    # Print header
    print 'TextVentures - About\n'

    # Print general information
    print 'A simple text-based adventure system.\n'

    # Print license information
    print 'TextVentures version ' + config.version
    print 'Copyright (C) 2013 Rafael Medina García (RMed)\n'

    print 'TextVentures comes with ABSOLUTELY NO WARRANYY. This is free'
    print 'software, and you are welcome to redistribute it under the'
    print 'conditions set by the GNU General Public License v2.0; please'
    print 'see the LICENSE file for details.\n'

    # Show actions
    print '[B]ack'

    # Wait for user input
    while True:
        # Key listener
        key_listener = Listener()
        key = key_listener()
        # Action parser
        action_parser = Action(key, 'about')
        action = action_parser()

