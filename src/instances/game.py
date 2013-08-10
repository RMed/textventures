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

import os, sys
import menu

class Game():
    """Main Game instance."""

    def __init__(self, game, conf_dir):
        """This instance is in charge of playing through the adventure.

        Arguments:
            game -- game object
            conf_dir -- configuration directory
        """

        # Define game
        self.game = game
        # Define adventure directory
        self.directory = os.path.join(conf_dir, 'adventures', 'stories',
                                game.get_dir())
        # Define the saves parser
        self.saves_parser = psaves.SavesParser(os.path.join(conf_dir, 
                                'adventures', 'saves.xml'))
        # Define scenario parser
        self.scenario = pscenario.Scenario(os.path.join(self.directory,
                                            game.get_progress()))

    def __call__(self):
        # Load the scenario
        self.load_scenario()

    def update_scenario(self, scenario):
        """Update current scenario.
        
        Arguments:
            scenario -- new scenario
        """

        # Update the progress
        self.game.set_progress(scenario)
        # Update the scenario
        self.scenario = pscenario.Scenario(os.path.join(self.directory,
                                              scenario))
        # Load the scenario
        self.load_scenario()

    def load_scenario(self):
        """Display the current scenario."""

        # Save progress
        self.saves_parser.save_game(self.game)

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
        
        # Get commands
        scenario_commands = self.scenario.get_commands()

        # Wait for user input
        while True:
            input_command = raw_input('-> ')
            self.perform_action(input_command, scenario_commands)
    
    def perform_action(self, input_command, command_list):
        """Perform an action.

        Check player's input and compare it with the command list.

        Arguments:
            input_command -- command entered by the user
            command_list -- available commands in the scenario
        """

        # Check if the user wants to leave
        if input_command == 'exit':
            # Go to main menu
            menu.main_menu()

        # Check the commands
        for command in command_list:
            if command.get_name() == input_command:
                # Command matches
                action = command.get_action()
                # Check what to do
                if action.get_type() == 'print':
                    # Print text
                    print action.get_content()
                    return
                else:
                    # Jump
                    self.update_scenario(action.get_content())
            
            # Default action to take
            if command.get_type() == 'default':
                default_action = command.get_action()

        # Did not perform any action
        if default_action.get_type() == 'print':
            # Print text
            print default_action.get_content()
            return
        else:
            # Jump
            self.update_scenario(default_action.get_content())
