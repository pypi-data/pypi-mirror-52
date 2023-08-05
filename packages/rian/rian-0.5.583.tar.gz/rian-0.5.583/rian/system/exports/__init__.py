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

__copyright__ = '2019 Frootlab'
__license__ = 'GPLv3'
__docformat__ = 'google'
__author__ = 'Frootlab Developers'
__email__ = 'contact@frootlab.org'
__authors__ = ['Patrick Michl <patrick.michl@frootlab.org>']

import rian.system.exports.archive

def filetypes(filetype = None):
    """Get supported system export filetypes."""

    type_dict = {}

    # get supported archive filetypes
    archive_types = rian.system.exports.archive.filetypes()
    for key, val in list(archive_types.items()):
        type_dict[key] = ('archive', val)

    if not filetype:
        return {key: val[1] for key, val in list(type_dict.items())}
    if filetype in type_dict:
        return type_dict[filetype]

    return False

def save(system, path = None, filetype = None, workspace = None,
    base = 'user', **kwds):
    """Export system to file.

    Args:
        system (object): rian system instance
        path (str, optional): path of export file
        filetype (str, optional): filetype of export file
        workspace (str, optional): workspace to use for file export

    Returns:
        Boolean value which is True if file export was successful

    """

    from hup.base import otree

    if not otree.has_base(system, 'System'):
        raise ValueError("system is not valid")

    from hup.base import env

    # get directory, filename and fileextension
    if isinstance(workspace, str) and not workspace == 'None':
        directory = rian.path('systems',
            workspace=workspace, base=base)
    elif isinstance(path, str):
        directory = env.get_dirname(path)
    else: directory = env.get_dirname(system.path)
    if isinstance(path, str):
        name = env.basename(path)
    else:
        name = system.fullname
    if isinstance(filetype, str):
        fileext = filetype
    elif isinstance(path, str):
        fileext = env.fileext(path) or env.fileext(system.path)
    else:
        fileext = env.fileext(system.path)
    path = str(env.join_path(directory, name + '.' + fileext))

    # get filetype from file extension if not given
    # and test if filetype is supported
    if not filetype:
        filetype = fileext.lower()
    if filetype not in filetypes():
        raise ValueError(
        f"filetype '{filetype}' is not supported.")

    # export to file
    module_name = filetypes(filetype)[0]
    if module_name == 'archive':
        return rian.system.exports.archive.save(
            system, path, filetype, **kwds)

    return False
