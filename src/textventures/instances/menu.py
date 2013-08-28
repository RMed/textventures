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

from .. parser import metadata, saves
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
    if not os.path.isdir(config.TEXTVENTURES_DIR):
        # Create the directory tree
        try:
            os.mkdir(config.TEXTVENTURES_DIR)
            os.mkdir(config.ADVENTURES_DIR)
        except:
            print _('Could not create configuration directory')

    # Print program information
    print _('TextVentures - Main Menu')
    print '\n'

    # Print navigation menu
    print _('[N] New game')
    print _('[L] Load game')
    print '\n'
    print _('[H] Help')
    print _('[A] About')
    print _('[E] Exit')

    # Wait for user input
    while True:
        # Key listener
        key_listener = Listener()
        key = key_listener()
        # Action parser
        action_parser = Action(key, 'main')
        action = action_parser()

def newgame_menu():
    """Display the new game menu.
    
    Show a list of available adventures and relevant information.
    """
    # Clear screen
    clear_screen()

    # Print header
    print _('TextVentures - New Game')
    print '\n'

    # Adventure list
    adventure_list = []

    # Get adventures
    adventure_list = metadata.get_adventures()

    # Print adventures
    if not adventure_list:
        print _('No adventures available')
    else:
        for index, adventure in enumerate(adventure_list):
            print str(index) + ')'
            print _('Title:') + ' ' + str(adventure.get_title())
            print _('Description:') + ' ' + str(adventure.get_description())
            print _('Author:') + ' ' + str(adventure.get_author())
            print _('Email:') + ' ' + str(adventure.get_email())
            print _('URL:') + ' ' + str(adventure.get_url())
            print _('Version:') + ' ' + str(adventure.get_version())
            print _('Compatibility:') + ' ' + \
                    str(adventure.get_compatible())
            print _('Languages:') + ' ' + \
                    ', '.join(adventure.get_locales())
            print '-----------------'

    # Show actions
    print '\n'
    print _('[C] Choose adventure to start')
    print _('[B] Back')

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
        input_num = raw_input(
                _('Please write an adventure number to load:') + ' ')

        # Check if the player wants to leave
        if input_num == 'MENU':
            newgame_menu()

        # Check if int
        try:
            game_index = int(input_num)
            # Check if out of bounds
            if game_index >= len(adventure_list):
                print _('Please write a valid number')
                continue
        except:
            print _('Please write a valid number')
            continue

        # Check if compatible
        if not adventure_list[game_index].get_compatible() == config.VERSION:
            print _('The adventure is not compatible with this version!')
            continue

        # Ask for the language if there are two or more
        if len(adventure_list[game_index].get_locales()) >= 2:
            while True:
                lang = raw_input(_('Please choose a language:') + ' ')
                # Check if language is in the list
                if not str(lang) in adventure_list[game_index].get_locales():
                    print _('Please choose an available language')
                else:
                    break
                    

        # Get directory
        adventure_dir = os.path.join(
                adventure_list[game_index].get_location(), str(lang))

        # Ask for an ID for the game
        input_id = raw_input(
                _('Please write an ID for this adventure:') + ' ')

        # Get the first scenario
        first = adventure_list[game_index].get_first()

        # Build game
        new_game = saves.Game(input_id, adventure_dir, first)

        # Load the game
        start_game = Play(new_game)
        game = start_game()

def load_menu():
    """Display the load game menu.

    Opens the saves file (if any) and shows all the games saved.
    The player must write the number of the game to load.
    """
    # Clear screen
    clear_screen()

    # Print header
    print _('TextVentures - Load Game')
    print '\n'

    # Saves list
    saves_list = []

    # Check if the saves file exists
    if not os.path.isfile(config.SAVES_FILE):
        try:
            # Need to create the file
            saves_tag = XML.Element('savefile')
            saves_tree = XML.ElementTree(saves_tag)
            saves_tree.write(config.SAVES_FILE)
        except:
            print _('Could not create the saves file')

    # Fill the list
    saves_list = saves.get_saves()

    # Print the saves (if any)
    if not saves_list:
        # No saved games
        print _('There are no saved games')
    else:
        # Print games
        for index, save in enumerate(saves_list):
            print str(index) + ')'
            print _('ID:') + ' ' + save.get_id()
            print _('Adventure:') + ' ' + save.get_dir()
            print _('Progress:') + ' ' + save.get_title()
            print '--------------'

    # Show actions
    print '\n'
    print _('[C] Choose game to load')
    print _('[B] Back')

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
        input_num = raw_input(
                _('Please write a game number to load:') + ' ')

        # Check if the player wants to leave
        if input_num == 'MENU':
            load_menu()

        # Check if int
        try:
            game_index = int(input_num)
            # Check if out of bounds
            if game_index >= len(saves_list):
                print _('Please write a valid number')
                continue
        except:
            print _('Please write a valid number')
            continue

        # Get ID
        adventure_id = saves_list[game_index].get_id()

        # Get directory
        adventure_dir = saves_list[game_index].get_dir()

        # Get the progress
        progress = saves_list[game_index].get_progress()

        # Get the title
        title = saves_list[game_index].get_title()

        # Build game
        loaded_game = saves.Game(adventure_id, adventure_dir, 
                progress, title)

        # Check if compatible
        game_file = os.path.join(config.ADVENTURES_DIR, adventure_dir,
                '..', 'metadventure.xml')
        game_tree = XML.parse(game_file)
        game_root = game_tree.getroot()
        if not game_root.find('compatible').text == config.VERSION:
            print _('The adventure is not compatible with this version!')
            continue

        # Load the game
        start_game = Play(loaded_game)
        game = start_game()

def help_menu():
    """Display the help menu.
    
    Briefly show how to navigate and play the adventures.
    """
    # Clear screen
    clear_screen()

    # Print header
    print _('TextVentures - Help')
    print '\n'

    # Print menu navigation help
    print _('--- MENU NAVIGATION ---')
    print _("Navigating through TextVenture's menus is fairly simple: "
            "in the different menus, you will see the available options "
            "of the form '[B] Back' (which, in this case, takes you back "
            "to the main menu). The character between the braces is the "
            "that must be pressed in order to perform that action.")
    print '\n'

    # Print game choosing help
    print _('--- CHOOSING A GAME ---')
    print _("In the New Game and Load Game menus, you are presented with "
            "several games that are available for playing. In order to "
            "play any of these games, you must first choose a game "
            "and then write the wished game number. If you enter this "
            "mode and want to leave, simply write MENU (in caps) and you "
            "will return to the menu mode.")
    print '\n'

    # Print adventure help
    print _('--- PLAYING ---')
    print _("While playing, the menu navigation keys will not work. "
            "Instead, you are presented with the prompt '->' and you will "
            "have to write the correct command in order to advance in the "
            "story. Note that there may be several commands for each of "
            "the scenarios. If you want to leave the game, simply write "
            "MENU (in caps) and you will be back in the main "
            "menu. The game is saved every time a scenario is loaded, so "
            "you do not need to worry about your progress being lost.")
    print '\n'

    # Show actions
    print _('[B] Back')

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
    print _('TextVentures - About')
    print '\n'

    # Print general information
    print _('A simple text-based adventure system.')
    print '\n'

    # Print license information
    print _('TextVentures version') + ' ' + config.VERSION
    print 'Copyright (C) 2013 Rafael Medina García (RMed)'
    print '\n'

    print "TextVentures comes with ABSOLUTELY NO WARRANYY. This is free"
    print "software, and you are welcome to redistribute it under the"
    print "conditions set by the GNU General Public License v2.0; please"
    print "see the LICENSE file for details."
    print '\n'

    # Show actions
    print _('[B] Back')

    # Wait for user input
    while True:
        # Key listener
        key_listener = Listener()
        key = key_listener()
        # Action parser
        action_parser = Action(key, 'about')
        action = action_parser()

