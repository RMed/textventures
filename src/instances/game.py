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

class Game():
    """Main Game instance."""

    def __init__(self, game, saves_parser):
        """This instance is in charge of playing through the adventure.

        Arguments:
            game -- Game object
        """

        # Define game
        self.game = game
        # Define adventure directory
        self.directory = os.path.join(os.path.expanduser('~'), 
                            '.textventures', 'adventures', 'stories',
                                game.get_dir())
        # Define the saves parser obtained from the menu
        self.saves_parser = saves_parser
        # Define scenario parser
        self.scenario = pscenario.Scenario(os.path.join(self.directory,
                                            game.get_progress()))

    def __call__(self):
        # Load the scenario
        self.load_scenario(self.scenario)

    def update_scenario(self, progress):
        """Update current scenario.
        
        Arguments:
            progress -- new progress
        """

        self.scenario = pscenario.Scenario(os.path.join(self.directory,
                                            progress))

    def load_scenario(self, scenario):
        """Display the current scenario.

        Arguments:
            scenario -- scenario parser to load
        """

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
        scenario_commands = self.scenario.get_comands()

        # Wait for user input
        while True:
            input_command = raw_input("-> ")

            # Check commands
            acted = False
            for command in scenario_commands:
                if command.get_name() == input_command:
                    # Command matches
                    action = command.get_action()
                    # Check what to do
                    if action.get_type() == 'print':
                        # Print text
                        print action.get_content()
                    else:
                        # Jump
                       self.update_scenario(action.get_content())
                       self.load_scenario(self.scenario)
                    # Action done
                    acted = True

                # Default action to take
                if command.get_type() == 'default':
                    default_action = command.get_action()

            # No action taken
            if not acted:
                if default_action.get_type() == 'jump':
                    # Jump
                    self.update_scenario(default_action.get_content())
                else:
                    # Print text
                    print default_action.get_content()

