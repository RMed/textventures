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

"""
This file contains global variables used across several modules. These
variables must not be modified by the program.
"""
import os

# Running directory
RUN_DIR = ''

# TextVentures directory in user folder
TEXTVENTURES_DIR = os.path.join(os.path.expanduser('~'), '.textventures')

# Adventure directory
ADVENTURES_DIR = os.path.join(TEXTVENTURES_DIR, 'adventures')

# Save file location
SAVES_FILE = os.path.join(TEXTVENTURES_DIR, 'saves.xml')

# Language configuration file
LANG_FILE = os.path.join(TEXTVENTURES_DIR, 'lang.conf')
# Language in use (read at startup)
LANG = ''
# Language list:
# These are added manually when a new language file is created. The name
# represents the locale code (directory).
LANG_LIST = ['en', 'es']

# Program version
VERSION = '0.2.1'

