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

from .. parser import scenario, saves
from .. import config

import os, sys
import menu

class Play():
    """Main Game instance."""

    def __init__(self, game):
        """This instance is in charge of playing through the adventure.

        Arguments:
            game -- game object
        """
        # Define game
        self.game = game
        # Define adventure directory
        self.directory = os.path.join(config.ADVENTURES_DIR, 
                game.get_dir())
        # Define scenario parser
        self.scenario = game.get_progress()

    def __call__(self):
        # Load the scenario
        self.update_scenario(self.scenario)

    def update_scenario(self, new_scenario):
        """Update current scenario.
        
        Arguments:
            scenario -- new scenario
        """
        # Update the progress
        self.game.set_progress(new_scenario)
        # Update the scenario
        self.scenario = scenario.Scenario(os.path.join(self.directory,
                new_scenario))
        # Update the title
        self.game.set_title(self.scenario.get_title())
        # Load the scenario
        self.load_scenario()

    def load_scenario(self):
        """Display the current scenario."""
        # Save progress
        saves.save_game(self.game)

        # Clear screen
        if sys.platform.startswith('win'):
            # Windows
            os.system('cls')
        else:
            # UNIX
            os.system('clear')

        # Print scenario title
        print self.scenario.get_title()
        print '\n'

        # Print paragraphs
        scenario_paragraphs = self.scenario.get_paragraphs()
        for p in scenario_paragraphs:
            print p
            print '\n'
        
        # Get actions 
        scenario_actions = self.scenario.get_actions()

        # Wait for user input
        while True:
            input_command = raw_input('-> ')
            self.perform_action(input_command, scenario_actions)
    
    def perform_action(self, input_command, action_list):
        """Perform an action.

        Check player's input and compare it with the command list.

        Arguments:
            input_command -- command entered by the user
            action_list -- available actions for the scenario
        """
        # Check if the user wants to leave
        if input_command == 'MENU':
            # Go to main menu
            menu.main_menu()

        # Check the actions
        for action in action_list:
            # Check if default action
            if action.get_input_type() == 'default':
                # Save in case it needs to be executed
                default_action = action
                continue

            # Check the commands
            for command in action.get_command_list():
                # Check if player's input is in the command list
                if input_command.lower().decode('utf8') == command.lower():
                    # Command match found
                    if action.get_action_type() == 'text':
                        # Print text
                        print action.get_content()
                        return
                    else:
                        # Jump
                        self.update_scenario(action.get_content())
            
        # Did not perform any action
        if default_action.get_action_type() == 'text':
            # Print text
            print default_action.get_content()
            return
        else:
            # Jump
            self.update_scenario(default_action.get_content())

