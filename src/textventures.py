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

import sys

class Listener:
    """Gets user input for navigation."""
    
    def __init__(self):
        # Check for Windows platform
        if sys.platform.startswith('win'):
            import msvcrt
        # Check for UNIX platforms
        else:
            import tty

    def __call__(self):
        # Windows
        if sys.platform.startswith('win'):
            import msvcrt
            # Save character
            char = msvcrt.getch()
        # UNIX
        else:
            import tty, termios
            # Read character
            fd = sys.stdin.fileno()
            attr = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                char = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, attr)
        # Return character
        return char

class Action:
    """Check the input character and act accordingly."""

    def __init__(self, input_char):
        self.char = input_char

    def __call__(self):
        # Check the character to see what to do
        if self.char == 'n':
            # New game
            print 'New game (to be implemented)'
        elif self.char == 'l':
            # Load game
            print 'Load game (to be implemented)'
        elif self.char == 'e':
            # Exit program
            sys.exit()

def main_menu():
    """Display the main menu.

    This function must check what keys have been pressed by the player
    for navigation purposes
    """

    # Print program information
    print 'TextVentures\n'

    # Print navigation menu
    print '(N)ew game'
    print '(L)oad game'
    print '(E)xit'

    # Main loop
    while True:
        # Key listener
        key_listener = Listener()
        key = key_listener()
        # Action parser
        action_parser = Action(key)
        action = action_parser()

if __name__ == "__main__":
    # Show main menu
    main_menu()

