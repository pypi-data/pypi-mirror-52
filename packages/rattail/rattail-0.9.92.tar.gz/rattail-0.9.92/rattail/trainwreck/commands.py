# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2019 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Trainwreck commands
"""

from __future__ import unicode_literals, absolute_import

import sys

from rattail import __version__
from rattail import commands
from rattail.util import load_object


def main(*args):
    """
    Primary entry point for Trainwreck command system
    """
    if args:
        args = list(args)
    else:
        args = sys.argv[1:]

    cmd = Command()
    cmd.run(*args)


class Command(commands.Command):
    """
    Primary command for Trainwreck
    """
    name = 'trainwreck'
    version = __version__
    description = "Trainwreck -- Transaction data warehouse"
    long_description = ""


class ImportToTrainwreck(commands.ImportSubcommand):
    """
    Generic base class for commands which import *to* a Trainwreck DB.
    """
    # subclass must set these!
    handler_key = None
    default_handler_spec = None

    def get_handler_factory(self, **kwargs):
        if self.config:
            spec = self.config.get('rattail.trainwreck.importing', '{}.handler'.format(self.handler_key),
                                   default=self.default_handler_spec)
        else:
            # just use default, for sake of cmd line help
            spec = self.default_handler_spec
        return load_object(spec)
