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
import os

class AdventureParser():
    """Adventure parser."""

    def __init__(self, conf_dir):
        """Creates an object that obtains the information of all the
        available adventures.
        """

        # Define the adventures directory
        self.adventures_dir = os.path.join(conf_dir, 'adventures')

    def get_adventures(self):
        """Get a list of adventures."""

        # Adventure list
        adventure_list = []

        # Get adventures
        for root, dirs, files in os.walk(self.adventures_dir):
            for adv in dirs:
                try:
                    # Parse adventure file
                    adventure_file = os.path.join(root, adv, 
                                                'metadventure.xml')
                    adventure_tree = XML.parse(adventure_file)
                    adventure_root = adventure_tree.getroot()

                    # Get information
                    title = adventure_root.find('title').text
                    desc = adventure_root.find('description').text
                    author = adventure_root.find('author').text
                    email = adventure_root.find('email').text
                    url = adventure_root.find('url').text
                    version = adventure_root.find('version').text
                    first = adventure_root.find('first').text
                    location = adv

                    new_adventure = Adventure(location, title, desc, author, email,
                                            url, version, first)

                    adventure_list.append(new_adventure)
                except:
                    # Error, skip continue with next
                    continue

        # Return adventure list
        return adventure_list

class Adventure(): 
    """Adventure object."""
    
    def __init__(self, location, title, desc, author, email, url, 
                    version, first):
        """Adventure constructor.

        Creates an object to represent the adventure

        Arguments:
            location -- directory name of the adventure
            title -- title of the adventure
            desc -- description of the adventure
            author -- author of the adventure
            email -- email of the author
            url -- url of the author
            version -- version of the adventure
            first -- first scenario of the adventure
        """
        
        # Define the information of the adventure
        self.location = location
        self.title = title
        self.description = desc
        self.author = author
        self.email = email
        self.url = url
        self.version = version
        self.first = first

    def get_location(self):
        """Get the location of the adventure."""
        return self.location

    def get_title(self):
        """Get the title of the adventure."""
        return self.title

    def get_description(self):
        """Get the description of the adventure."""
        return self.description

    def get_author(self):
        """Get the author of the adventure."""
        return self.author

    def get_email(self):
        """Get the email of the author (optional field)."""
        return self.email

    def get_url(self):
        """Get the support url (optional field)."""
        return self.url

    def get_version(self):
        """Get the version of the adventure."""
        return self.version

    def get_first(self):
        """Get the first scenario of the adventure."""
        return self.first

