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
"""Scatter Plots."""

__copyright__ = '2019 Frootlab'
__license__ = 'GPLv3'
__docformat__ = 'google'
__author__ = 'Frootlab Developers'
__email__ = 'contact@frootlab.org'
__authors__ = ['Patrick Michl <patrick.michl@frootlab.org>']

import numpy as np
from rian.plot import Plot

class Scatter2D(Plot):
    """ """

    _config = {
        'grid': True,
        'pca': True
    }

    @staticmethod
    def _pca2d(x):
        """Calculate projection to largest two principal components."""
        # get dimension of array
        dim = x.shape[1]

        # calculate covariance matrix
        cov = np.cov(x.T)

        # calculate eigevectors and eigenvalues
        vals, vecs = np.linalg.eig(cov)

        # sort eigevectors by absolute eigenvalues
        pairs = [(np.abs(vals[i]), vecs[:, i]) for i in range(len(vals))]
        pairs.sort(key=lambda x: x[0], reverse=True)

        # calculate projection matrix
        proj = np.hstack(
            [pairs[0][1].reshape(dim, 1), pairs[1][1].reshape(dim, 1)])

        # calculate projection
        parray = np.dot(x, proj)

        return parray

    def plot(self, x):
        """ """

        # test arguments
        if x.shape[1] != 2:
            if self._config['pca']:
                x = self._pca2d(x)
            else: raise TypeError(
                "first argument is required to be an array of shape (n, 2)")

        x_1, x_2 = x[:, 0], x[:, 1]

        # plot grid
        self._axes.grid(self._config['grid'])

        # plot scattered data
        self._axes.scatter(x_1, x_2)

        # (optional) plot title
        self.plot_title()

        return True
