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

class AdventureParser(): 
    """Adventure XML file parser.

    The XML file must contain a title, a description, the name of the
    author, the email of the author (optional), the support url (optional)
    and a version number.
    """
    
    def __init__(self, adventure_file):
        """AdventureParser constructor.

        Creates an object from which to obtain the necessary information
        of the adventure

        Arguments:
            adventure_file -- path to the xml file to parse
        """
        # Define the contents of the adventure file
        self.adventure_tree = XML.parse(adventure_file)
        # Find the root of the xml tree
        self.adventure_root = self.adventure_tree.getroot()

    def get_title(self):
        """Get the title of the adventure."""
        return self.adventure_root.find('title').text

    def get_description(self):
        """Get the description of the adventure."""
        return self.adventure_root.find('description').text

    def get_author(self):
        """Get the author of the adventure."""
        return self.adventure_root.find('author').text

    def get_email(self):
        """Get the email of the author (optional field)."""
        return self.adventure_root.find('email').text

    def get_url(self):
        """Get the support url (optional field)."""
        return self.adventure_root.find('url').text

    def get_version(self):
        """Get the version of the adventure."""
        return self.adventure_root.find('version').text

