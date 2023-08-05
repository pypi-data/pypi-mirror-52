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
import networkx

def filetypes():
    """Get supported graph filetypes for network export."""
    return {
        'gml': 'Graph Modelling Language',
        'graphml': 'Graph Markup Language',
        'xml': 'Graph Markup Language',
        'dot': 'GraphViz DOT'
    }

def save(network, path, filetype, **kwds):
    """Export network to graph description file."""

    # test if filetype is supported
    if filetype not in filetypes():
        raise ValueError(f"filetype '{filetype}' is not supported")

    # create path if not available
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))

    # get networkx graph from network
    graph = network.get('graph', type='graph')

    if filetype == 'gml':
        return Gml(**kwds).save(graph, path)
    if filetype in ['graphml', 'xml']:
        return Graphml(**kwds).save(graph, path)
    if filetype == 'dot':
        return Dot(**kwds).save(graph, path)

    return False

def _graph_encode(graph, coding=None):
    """Encode graph parameters."""
    from hup.base import binary

    # no encoding
    if not isinstance(coding, str) or coding.lower() == 'none':
        return graph._graph.copy()

    # base64 encoding
    if coding.lower() == 'base64':

        # encode graph 'params' dictionary
        graph.graph['params'] = binary.pack(
            graph.graph['params'], encoding='base64')

        # encode nodes 'params' dictionaries
        for node in graph.nodes():
            graph.node[node]['params'] = binary.pack(
                graph.node[node]['params'], encoding='base64')

        # encode edges 'params' dictionaries
        for edge in graph.edges():
            graph.edges[edge]['params'] = binary.pack(
                graph.edges[edge]['params'], encoding='base64')

        # set flag for graph parameter coding
        graph.graph['coding'] = 'base64'
        return graph

    raise ValueError("""could not encode graph parameters:
        unsupported coding '%s'.""" % coding)

class Gml:
    """Export network to GML file."""

    settings = None
    default = {'coding': 'base64'}

    def __init__(self, **kwds):
        self.settings = {**self.default, **kwds}

    def save(self, graph, path):
        # encode graph parameter dictionaries
        graph = _graph_encode(graph, coding=self.settings['coding'])

        # write networkx graph to gml file
        networkx.write_gml(graph, path)

        return path

class Graphml:
    """Export network to GraphML file."""

    settings = None
    default = {'coding': 'base64'}

    def __init__(self, **kwds):
        self.settings = {**self.default, **kwds}

    def save(self, graph, path):

        # encode graph parameter dictionaries
        graph = _graph_encode(graph, coding=self.settings['coding'])

        # write networkx graph to gml file
        networkx.write_graphml(graph, path)

        return path

class Dot:
    """Export network to GraphViz Dot file."""

    settings = None
    default = {'coding': 'base64'}

    def __init__(self, **kwds):
        self.settings = {**self.default, **kwds}

    def save(self, graph, path):

        # encode graph parameter dictionaries
        graph = _graph_encode(graph, coding=self.settings['coding'])

        # check library support for dot files
        try:
            from networkx.drawing import nx_pydot
        except ImportError as err:
            raise ValueError(
                "could not export graph in 'dot' format: "
                "requires packages 'pygraphviz' and 'pydot'") from err

        # write networkx graph to graphviz dot file
        nx_pydot.write_dot(graph, path)

        return path
