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

class ScenarioParser():
    """Scenario XML file parser.

    The XML file contains a title that is displayed on top, text paragraphs
    to display and a list of available commands for the player.
    """
    
    def __init__(self, scenario_file):
        """Scenario parser.

        Creates an object from which to obtain the necessary information
        of the scenario

        Arguments:
            scenario_file -- path to the xml file to parse
        """
        # Define the contents of the xml file
        self.scenario_tree = XML.parse(scenario_file)
        # Find the root of the xml tree
        self.scenario_root = self.scenario_tree.getroot()

    def get_title(self):
        """Get the title of the scenario."""
        return self.scenario_root.find('title').text

    def get_paragraphs(self):
        """Get the text paragraphs to be written on screen."""
        paragraph_list = []

        # Loop through the paragraphs
        for paragraph in self.scenario_root.findall('scenariop'):
            # Append the paragraph to the list
            paragraph_list.append(paragraph.text)

        # Return paragraph list
        return paragraph_list

    def get_commands(self):
        """Get the available commands for the scenario."""
        command_list = []
        
        # Loop through the commands
        for command in self.scenario_root.findall('command'):
            # Get type attribute
            command_type = command.get('type')
            # Get command name if type is 'input'
            if command_type == 'input':
                command_name = command.get('name')
            else:
                command_name = None

            # Parse action of the command
            # TODO: enable the use of multiple actions
            action = command.find('action')
            # Get action type
            action_type = action.get('type')
            # Get action content
            action_content = action.text

            # Construct the action
            scenario_action = ScenarioAction(action_type, action_content)
            # Construct the command
            scenario_command = ScenarioCommand(command_type, command_name, scenario_action)

            # Add the command to the list
            command_list.append(scenario_command)

        # Return command list
        return command_list

class ScenarioCommand():
    """Command that can be used by the player.

    The type of commands available are:

    input -- executed when the player's input matches the command name
    default -- executed when the player's input was not recognized
    """

    def __init__(self, parsed_type, parsed_name, parsed_action):
        """Command object.

        Creates an object from the parsed information of the command.

        Arguments:
            parsed_type -- command type
            parsed_action -- action attached to the command
            parsed_name -- command name, available with type 'input'
        """
        # Define command type
        self.command_type = parsed_type
        # Define command name (not necessary if type is 'default')
        self.command_name = parsed_name
        # Define action attached to the command
        self.command_action = parsed_action

    def get_type(self):
        """Get command type."""
        return self.command_type

    def get_name(self):
        """Get command name."""
        return self.command_name

    def get_action(self):
        """Get action to perform"""
        return self.command_action

class ScenarioAction():
    """Action attached to a command.

    The type of actions available are:

    print -- print a text on screen
    jump -- jump to another scenario
    """

    def __init__(self, parsed_type, parsed_content):
        """Action object.

        Creates an object from the parsed information of the action.

        Arguments:
            parsed_type -- action type
            parsed_content -- action content, may be a text or a scenario
        """
        # Define action type
        self.action_type = parsed_type
        # Define action content
        self.action_content = parsed_content

    def get_type(self):
        """Get action type."""
        return self.action_type

    def get_content(self):
        """Get the content of the action, may be a text or a jump
        destination.
        """
        return self.action_content

