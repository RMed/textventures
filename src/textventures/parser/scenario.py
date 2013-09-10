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

class Scenario():
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

    def get_actions(self):
        """Get the available actions for the scenario."""        
        action_list = []

        # Loop through the actions
        for action in self.scenario_root.findall('action'):
            # Get input type
            input_type = action.get('input')
            # Get action type
            action_type = action.get('type')
            # Get content
            action_content = action.get('content')

            # Get a list of commands
            command_list = []
            # Loop through the commands
            for command in action.iter('command'):
                # Add command to list
                command_list.append(command.text)

            # Create ScenarioAction object
            new_action = ScenarioAction(input_type, action_type,
                    action_content, command_list)

            # Add action to list
            action_list.append(new_action)

        # Return list
        return action_list

class ScenarioAction():
    """Available action in the scenario.

    An action may have as many commands attached as needed, meaning that
    any of the commands specified will trigger the action.

    The 'input' tag specifies if the action is to be performed when the
    player issues a known command (player) or when the command is not
    recognized (default). There can only be one default action.

    The 'type' tag shows the kind of action to perform. The available types
    are 'jump', which leads to another scenario and has an extra tag
    'target', or 'text', which prints a message on screen.
    """

    def __init__(self, input_type, action_type, content, command_list):
        """ScenarioAction object.

        Arguments:
            input_type -- whether the action is performed when player
                issues a command (player) or when the command is not
                recognized (default)
            action_type -- whether the action prints text on screen
                (text) or loads another scenario (jump)
            command_list -- commands attached to the action
            content -- jump destination or text to print
        """
        self.input_type = input_type
        self.action_type = action_type
        self.content = content
        self.command_list = command_list

    def get_input_type(self):
        """Get the input type"""
        return self.input_type

    def get_action_type(self):
        """Get the action type"""
        return self.action_type

    def get_content(self):
        """Get action content"""
        return self.content

    def get_command_list(self):
        """Get the command list"""
        return self.command_list

