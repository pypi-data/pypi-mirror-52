# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 19:06:45 2016

@author: Falaize
"""
from pyphs import Graph
from pyphs.dictionary.tools import mappars, nicevarlabel


class Connector(Graph):
    """
    class for gyrators and transformers
    """
    def __init__(self, label, nodes, **kwargs):
        # init PortHamiltonianObject
        Graph.__init__(self, label=label)
        # pop connector type
        connector_type = kwargs.pop('connector_type')
        # build correspondance between labels in subs and pars (dicpars)...
        # ... and build the correspondance between symbols and subs (subs)
        dicpars, subs = mappars(self, **kwargs)
        # update dict of subs in phs
        self.core.subs.update(subs)
        # replace parameters in alpha by correspondances in 'dicpars'
        alpha = self.core.symbols('alpha')
        alpha = alpha.subs(dicpars)
        # symbols for inputs and outputs:
        u1, u2 = self.core.symbols([nicevarlabel('u', label + str(el))
                                    for el in (1, 2)])
        y1, y2 = self.core.symbols([nicevarlabel('y', label + str(el))
                                    for el in (1, 2)])
        # add connector component
        ny = self.core.dims.y()
        self.core.add_ports((u1, u2), (y1, y2))
        self.core.add_connector((ny, ny+1), alpha)
        # update phs.Graph with edges
        edge1_data = {'type': 'connector',
                      'connector_type': connector_type,
                      'alpha': alpha,
                      'ctrl': '?',
                      'label': y1,
                      'link': y2}
        edge2_data = {'type': 'connector',
                      'connector_type': connector_type,
                      'alpha': None,
                      'ctrl': '?',
                      'label': y2,
                      'link': y1}
        N1, N2, N3, N4 = nodes
        edges = [(N1, N2, edge1_data), (N3, N4, edge2_data)]
        # update phs.Graph with edges
        self.add_edges_from(edges)
