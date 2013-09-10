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
import os
import msgfmt

class BuildTranslations(Command):
    description = "compile .po translations and add them to the build"
    user_options = []

    def initialize_options(self):
        pass
 
    def finalize_options(self):
        pass

    def run(self):
        # Directory that contains the .po files
        po_dir = os.path.abspath(os.path.join(
                os.path.dirname(__file__), os.pardir, 'po'))
        # Build directory
        build_dir = os.path.abspath(os.path.join(
                os.path.dirname(__file__), os.pardir, 'build',
                    'textventures', 'locale'))
        # Create build directory if it does not exist
        if not os.path.exists(build_dir):
            os.makedirs(build_dir)

        # Loop the directory
        for path, names, filenames in os.walk(po_dir):
            for lang_file in filenames:
                # Check if .po files
                if lang_file.endswith('.po'):
                    # Get locale code
                    locale = lang_file[:-3]
                # Not a .po file
                else:
                    # Skip to next
                    continue

                lang_src = os.path.join(path, lang_file)
                # Set destination path
                lang_dst_dir = os.path.join(build_dir, locale,
                        'LC_MESSAGES')
                # Set destination file
                lang_dst_file = os.path.join(lang_dst_dir,
                        'textventures.mo')

                # Create directory if needed
                if not os.path.exists(lang_dst_dir):
                    os.makedirs(lang_dst_dir)

                # Compile translations
                if not os.path.exists(lang_dst_file):
                    print 'Compile ' + locale + '...'
                    msgfmt.make(lang_src, lang_dst_file)
                else:
                    # Check already existing translation to see if it
                    # needs to be recompiled.
                    src_mtime = os.stat(lang_src)[8]
                    dst_mtime = os.stat(lang_dst_file)[8]
                    if src_mtime > dst_mtime:
                        # Recompile
                        print 'Compile ' + locale + '...'
                        msgfmt.make(lang_src, lang_dst_file)

