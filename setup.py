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

from distutils.command.build import build as _build
from distutils.core import setup
from tools import build_trans, build_clean
import shutil

# Override the default build function to include the compilation of the
# translation files
class build(_build):
    # Add custom commands
    sub_commands = _build.sub_commands + [('build_locale', None)]

    def run(self):
        _build.run(self)
        # Copy LICENSE and AUTHORS files
        shutil.copy('LICENSE', self.build_lib)
        shutil.copy('AUTHORS', self.build_lib)

setup(
    # Standard information
    name='TextVentures',
    version='0.2.1',
    description='A simple text-based adventure system',
    author='Rafael Medina García (RMed)',
    author_email='rafamedgar@gmail.com',
    url='http://github.com/RMed/textventures',
    license = 'GPLv2',

    # Extra files for distribution
    data_files=[('', ['LICENSE', 'AUTHORS'])],
    # Packages to build
    packages = ['textventures', 'textventures.parser', 
            'textventures.instances'],
    # Set package source root location
    package_dir = {'': 'src'},
    # Include main module
    py_modules = ['textventures'],

    # Custom commands
    cmdclass = {
        'build': build,
        'build_locale': build_trans.BuildTranslations,
        'clean': build_clean.CleanBuild
    },

    # Build options
    options = {
        # Platform independent, use build directory directly
        'build': { 'build_lib': 'build' } 
    })

