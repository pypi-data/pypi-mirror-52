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

import imp
import rian
import os

class Workspace(object):
    """Rian workspace class."""

    _config    = None
    _default   = {}
    _attr_meta = {'name': 'r', 'about': 'rw', 'path': 'r', 'base': 'r'}

    def __getattr__(self, key):
        """Attribute wrapper to getter methods."""

        if key in self._attr_meta:
            if 'r' in self._attr_meta[key]: return self._get_meta(key)
            raise Warning(
                "attribute '%s' is not readable.")

        raise AttributeError('%s instance has no attribute %r'
            % (self.__class__.__name__, key))

    def __setattr__(self, key, val):
        """Attribute wrapper to setter methods."""

        if key in self._attr_meta:
            if 'w' in self._attr_meta[key]:
                return self._set_meta(key, val)
            raise Warning(
                "attribute '%s' is not writeable." % key)

        self.__dict__[key] = val

    def __init__(self, *args, **kwds):
        """Import object configuration and content from dictionary."""

        self._set_copy(**kwds)

    def get(self, key = 'name', *args, **kwds):
        """Get meta data of workspace."""

        # meta information
        if key in self._attr_meta: return self._get_meta(key)

        raise KeyError(f"unknown key '{key}'")

    def _get_meta(self, key):
        """Get meta information like 'name' or 'path'."""

        if key == 'about': return self._get_about()
        if key == 'base': return self._get_about()
        if key == 'name': return self._get_name()
        if key == 'path': return self._get_path()

        raise KeyError(f"unknown key '{key}'")

    def _get_about(self):
        """Get description.

        Short description of the content of the resource.

        Returns:
            Basestring containing a description of the resource.

        """

        return self._config.get('about', None)

    def _get_base(self):
        """Get workspace base."""

        return self._config.get('base', None)

    def _get_name(self):
        """Get name."""

        return self._config.get('name', None)

    def _get_path(self):
        """Get path."""

        return self._config.get('path', None)

    def set(self, key = None, *args, **kwds):
        """Set meta data of workspace."""

        # set meta information
        if key in self._attr_meta:
            return self._set_meta(key, *args, **kwds)

        # import workspace configuration configuration and dataset tables
        if key == 'copy': return self._set_copy(*args, **kwds)
        if key == 'config': return self._set_config(*args, **kwds)

        raise KeyError(f"unknown key '{key}'")

    def _set_meta(self, key, *args, **kwds):
        """Set meta information like 'name' or 'path'."""

        if key == 'about': return self._set_about(*args, **kwds)

        raise KeyError(f"unknown key '{key}'")

    def _set_about(self, val):
        """Set description."""

        if not isinstance(val, str): raise Warning(
            "attribute 'about' requires datatype 'basestring'.")
        self._config['about'] = val

        return True

    def _set_copy(self, config = None):
        """Set workspace configuration and dataset tables.

        Args:
            config (dict or None, optional): workspace configuration

        Returns:
            Bool which is True if and only if no error occured.

        """

        retval = True

        if config: retval &= self._set_config(config)

        return retval

    def _set_config(self, config = None):
        """Set configuration of workspace.

        Args:
            config (dict or None, optional): workspace configuration

        Returns:
            Bool which is True if and only if no error occured.

        """

        # initialize configuration dictionary
        if not self._config:
            self._config = self._default.copy()

        # update configuration dictionary
        if not config:
            return True

        self._config = {**self._config, **config}

        return True

    def list(self, type):
        """Return a list of known objects."""

        return rian.list(type,
            workspace = self._get_name(), base = self._get_base())
