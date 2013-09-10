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

from distutils.core import Command
import shutil, os

class CleanBuild(Command):
    description = "clean previous builds"
    user_options = []

    def initialize_options(self):
        self.cwd = None
 
    def finalize_options(self):
        self.cwd = os.getcwd()

    def run(self):
        # Check if in root directory
        assert os.getcwd() == self.cwd, 'Must be in root directory: %s' \
                % self.cwd

        # Get build and dist paths
        build = os.path.join(self.cwd, 'build')
        dist = os.path.join(self.cwd, 'dist')

        # Check if build exists
        if os.path.isdir(build):
            shutil.rmtree(build)

        # Check if dist exists
        if os.path.isdir(dist):
            shutil.rmtree(dist)

