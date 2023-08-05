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
"""Command line interface."""

__copyright__ = '2019 Frootlab'
__license__ = 'GPLv3'
__docformat__ = 'google'
__author__ = 'Frootlab Developers'
__email__ = 'contact@frootlab.org'
__authors__ = ['Patrick Michl <patrick.michl@frootlab.org>']

import getopt
import sys
from typing import Any
from hup.base import env
from rian.core import ui
from rian.core.ui import shell
from hup.typing import BoolOp
import rian

def print_scripts(workspace: str) -> None:
    """Print list of scripts to standard output."""
    rian.set('mode', 'silent')

    if rian.open(workspace):
        ui.info('Scripts in workspace %s:\n' % (rian.get('workspace')))
        for script in rian.list('scripts'):
            ui.info('    %s' % (script))
        ui.info('')

def print_usage() -> None:
    """Print script usage to standard output."""
    ui.info("Usage: rian [options]\n\n"
        "Options:\n\n"
        "    -h --help         "
        "      Print this\n"
        "    -s --shell        "
        "      Start rian session in IPython interactive shell\n"
        "    -l --list         "
        "      List workspaces\n"
        "    -w --workspace    "
        "      List scripts in workspace\n"
        "    -r --run-script   "
        "      Open workspace and execute script\n"
        "    -a --arguments    "
        "      Arguments passed to script\n"
        "    -v --version      "
        "      Print version")

def print_version() -> None:
    """Print rian version to standard output."""
    version = env.get_var('version') or ''
    ui.info('rian ' + version)

def print_workspaces() -> None:
    """Print list of workspaces to standard output."""
    rian.set('mode', 'silent')
    workspaces = rian.list('workspaces', base='user')
    ui.info('Workspaces:\n')
    for workspace in workspaces:
        ui.info('    %s' % (workspace))
    ui.info('')

def run_script(workspace: str, script: str, *args: Any) -> bool:
    """Run rian python script."""
    return rian.open(workspace) and rian.run(script, *args)

def run_shell() -> None:
    """Start rian session in IPython interactive shell."""
    name = env.get_var('name') or ''
    version = env.get_var('version') or ''
    banner = name + ' ' +  version
    shell.run(banner=banner)

def main() -> Any:
    """Launch rian."""
    argv = sys.argv[1:]
    if not argv:
        return run_shell()

    # Get command line options
    short = "hvslw:s:a:"
    long = ["workspace=", "script=", "arguments="]
    try:
        opts, args = getopt.getopt(argv, short, long)
    except getopt.GetoptError:
        return print_usage()

    dic = dict(opts)
    keys = dic.keys()
    given: BoolOp = (lambda *args: not keys.isdisjoint(set(args)))

    workspace = dic.get('-w') or dic.get('--workspace')
    script = dic.get('-r') or dic.get('--run-script')
    arguments = dic.get('-a') or dic.get('--arguments')

    if given('-h', '--help'):
        return print_usage()
    if given('-v', '--version'):
        return print_version()
    if given('-s', '--shell'):
        return run_shell()
    if given('-l', '--list'):
        return print_workspaces()

    if not workspace:
        return print_workspaces()
    if not script:
        return print_scripts(workspace)
    if not arguments:
        return run_script(workspace, script)
    return run_script(workspace, script, arguments)

if __name__ == "__main__":
    main()
