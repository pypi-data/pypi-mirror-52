# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Frootlab
# Copyright (C) 2013-2019 Patrick Michl
#
# This file is part of Rian, https://www.frootlab.org/rian
#
#  Rian is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rian is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
#  A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License along with
#  Rian. If not, see <http://www.gnu.org/licenses/>.
#
"""Runner script for unittests."""

__copyright__ = '2019 Frootlab'
__license__ = 'GPLv3'
__docformat__ = 'google'
__author__ = 'Frootlab Developers'
__email__ = 'contact@frootlab.org'
__authors__ = ['Patrick Michl <patrick.michl@frootlab.org>']

import fnmatch
import importlib
import os
import sys
import unittest
from hup.base import pkg
from rian.core import ui

#
# Script Configuration
#

package_name = 'rian'

#
# Runner Script
#

if __name__ == "__main__":
    argv = sys.argv[1:]
    module = argv[0] if argv else None

    # Import package and tests
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.insert(0, path)
    package = importlib.import_module(package_name)
    tests = importlib.import_module('tests')

    # Search and filter TestCases within tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    cases = pkg.search(
        module=tests, classinfo=unittest.TestCase, val='reference', errors=True)
    for ref in cases.values():
        if module:
            if not hasattr(ref, 'module'):
                continue
            if not hasattr(ref.module, '__name__'):
                continue
            if not fnmatch.fnmatch(ref.module.__name__, f'*{module}*'):
                continue
        suite.addTests(loader.loadTestsFromTestCase(ref))

    # Initialize TestRunner and run TestCases
    package_version = getattr(package, '__version__', '')
    ui.info(f"testing {package_name} {package_version}")
    cur_level = ui.get_notification_level()
    ui.set_notification_level('CRITICAL')
    runner = unittest.TextTestRunner(stream=sys.stderr, verbosity=2)
    try:
        runner.run(suite)
    finally:
        ui.set_notification_level(cur_level)
