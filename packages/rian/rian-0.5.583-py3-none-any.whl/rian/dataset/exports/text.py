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

import os
from hup.io import csv, ini
from rian.base import array

def filetypes() -> dict:
    """Get supported text filetypes for dataset export."""
    return {
        'csv': 'Comma Separated Values',
        'tsv': 'Tab Separated Values',
        'tab': 'Tab Separated Values'}

def save(dataset, path, filetype, **kwds):
    """Export dataset to archive file."""

    # test if filetype is supported
    if filetype not in filetypes():
        raise ValueError(f"filetype '{filetype}' is not supported")

    # create path if not available
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))

    if filetype == 'csv':
        return Csv(**kwds).save(dataset, path)
    if filetype in ['tsv', 'tab']:
        return Tsv(**kwds).save(dataset, path)

    return False

class Csv:
    """Export dataset to Comma Separated Values."""

    settings = None
    default = {'delim': ','}

    def __init__(self, **kwds):
        self.settings = {**self.default, **kwds}

    def save(self, dataset, path):

        # Create the configuration which is included in the CSV file
        # as initial comment lines
        keys = ['name', 'branch', 'version', 'about', 'author', 'email',
            'license', 'filetype', 'application', 'preprocessing',
            'type', 'labelformat']
        config = {}
        for key, val in dataset.get('config').items():
            if key in keys:
                config[key] = val

        # prepare CSV parameters and write CSV file
        comment = ini.encode(config, flat=True).strip('\n')
        delimiter = self.settings['delim']
        cols, data = dataset.get('data', output=('cols', 'recarray'))
        header = [''] + cols
        values = array.as_tuples(data)

        # Convert recarray to list of tuples
        return csv.save(path, header=header, values=values,
            comment=comment, delimiter=delimiter)

class Tsv(Csv):
    """Export dataset to Tab Separated Values."""

    default = {'delim': '\t'}
