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

import menu, sys

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

    def __init__(self, input_char, action_type):
        """Arguments:
                input_char -- pressed character
                action_type -- type of the action (menu, load, etc)
        """
        self.char = input_char.lower()
        self.action = action_type

    def __call__(self):
        # Check the action type
        if self.action == 'main':
            # Main menu
            if self.char == 'n':
                # New game menu
                menu.newgame_menu()
            elif self.char == 'l':
                # Load game menu
                menu.load_menu()
            elif self.char == 'o':
                # Options menu
                menu.options_menu()
            elif self.char == 'h':
                # Help menu
                menu.help_menu()
            elif self.char == 'a':
                # About menu
                menu.about_menu()
            elif self.char == 'e':
                # Exit program
                sys.exit()

        elif self.action == 'load':
            # Load menu
            if self.char == 'b':
                # Back to main menu
                menu.main_menu()
            elif self.char == 'c':
                # Choose game
                return self.char

        elif self.action == 'options':
            # Load menu
            if self.char == 'b':
                # Back to main menu
                menu.main_menu()
            elif self.char == 'c':
                # Choose language
                return self.char

        elif self.action == 'new':
            # New game menu
            if self.char == 'b':
                # Back to main menu
                menu.main_menu()
            elif self.char == 'c':
                # Choose game
                return self.char

        elif self.action == 'help':
            # Help menu
            if self.char == 'b':
                # Back to main menu
                menu.main_menu()

        elif self.action == 'about':
            # About menu
            if self.char == 'l':
                menu.show_license()
            elif self.char == 'b':
                # Back to main menu
                menu.main_menu()

        elif self.action == 'license':
            # License
            if self.char == 'b':
                # Back to About menu
                menu.about_menu()

