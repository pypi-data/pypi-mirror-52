# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 08:50:42 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import os
import ast
from pyphs.config import datum, VERBOSE

def sep():
    return ','


class Netlist:
    """
    Data structure for netlist elements. Each line of the netlist describes a\
 component, with data structured a follows
    > dic.comp label N1, N2, ..., Nn: par1=(lab, val) par2=val par3=lab
    where
    * component 'comp' is a module of dictionary 'dictionary.dic',
    * label is the component label (avoid creativity in chosen characters),
    * the N's are the nodes labels, which can be strings or numbers,
    * the par's are parameters identifiers defined in the component
    * lab is a new string label for the parameter,
    * val is a numerical value for the parameter.

    If no numerical value is provided, the parameter will be defined as a \
free-parameter that can be continuously controlled during the simulations. \
Else if no label is provided for the new component, the new label for the \
i-th parameter is defined as 'label_pari'.
    """
    def __init__(self, path, clear=False):
        """
        init with path to read data from.
        """
        n = path[path.rfind(os.sep)+1:]
        f = path[:path.rfind(os.sep)+1]
        if len(n) == 0:
            n, f = f, n
        if VERBOSE >= 1:
            print('Read netlist {}'.format(n))
            print('from folder {}'.format(f))
        self.path = path
        if not os.path.isfile(self.path) or clear:
            file_ = open(self.path, 'w')
            file_.close()
        self.datum = datum
        self.dictionaries = tuple()
        self.components = tuple()
        self.labels = tuple()
        self.nodes = tuple()
        self.arguments = tuple()
        self.read()

    # --------------------------------------------------------------------------
    # Folder

    def get_folder(self):
        return self.path[:self.path.rfind(os.sep)]

    folder = property(get_folder)

    # --------------------------------------------------------------------------
    # Filename

    def get_filename(self):
        return  self.path[self.path.rfind(os.sep)+1:]

    filename = property(get_filename)

    # --------------------------------------------------------------------------

    def __getitem__(self, n):
        item = {'dictionary': self.dictionaries[n],
                'component': self.components[n],
                'label': self.labels[n],
                'nodes': self.nodes[n],
                'arguments': self.arguments[n]}
        return item

    def __add__(net1, net2):
        net = net1
        for l in net2:
            net.add_line(l)
        return net

    def nlines(self):
        """
        return the number of lines in the netlist (i.e. the number of \
components).
        """
        return len(self.components)

    def add_line(self, dic):
        self.dictionaries = list(self.dictionaries)+[dic['dictionary'], ]
        self.components = list(self.components)+[dic['component'], ]
        self.labels = list(self.labels)+[dic['label'], ]
        self.nodes = list(self.nodes)+[dic['nodes'], ]
        self.arguments = list(self.arguments)+[dic['arguments'], ]

    def read(self):
        """
        read data from netlist
        """
        with open(self.path, "r") as openfileobject:
            for i, line in enumerate(openfileobject.readlines()):
                if line.startswith('#'):
                    if VERBOSE >= 1:
                        print('pass "{}"'.format(line[:-1]))
                elif len(line) == 1:
                    pass
                else:
                    if VERBOSE >= 1:
                        print('read "{}"'.format(line[:-1]))
                    # get 'infos' (dic, comp and nodes) and parameters
                    infos, _, parameters = line.partition(':')
                    # get ‘dic.comp' and 'label nodes'
                    si = infos.split()
                    diccomp = si.pop(0)
                    label = si.pop(0)
                    nodes = ''.join(si)
                    dic, _, comp = diccomp.partition('.')
                    self.dictionaries = list(self.dictionaries)+[dic, ]
                    self.components = list(self.components)+[comp, ]
                    self.labels = list(self.labels)+[label, ]
                    self.nodes = list(self.nodes)+[ast.literal_eval(nodes), ]
                    nb_pars = parameters.count('=')
                    pars = {}
                    for n in range(nb_pars):
                        par, _, parameters = parameters.partition(';')
                        par = par.replace(' ', '')
                        key, _, value = par.partition('=')
                        if value.startswith('('):
                            value = value[1:-1].split(',')
                            value = tuple(map(eval, value))
                        else:
                            try:
                                value = ast.literal_eval(value)
                            except ValueError:
                                pass
                        pars.update({key: value})
                    self.arguments = list(self.arguments)+[pars, ]

    def netlist(self):
        """
        Return the netlist as a formated string
        """
        netlist = ""
        for n in range(self.nlines()):
            netlist += self.line(n)
        return netlist[:-1]

    def write(self, path=None):
        """
        write the content of the netlist to file point by 'path'
        """
        if path is None:
            path = self.path
        file_ = open(path, 'w')
        file_.write(self.netlist())  # remove the last cariage return
        file_.close()

    def line(self, n):
        """
        print the netlist line 'n' whith appropriate format
        """
        return print_netlist_line(self[n])

    def delline(self, n):
        """
        delete the netlist line 'n'
        """
        self.dictionaries.pop(n)
        self.components.pop(n)
        self.labels.pop(n)
        self.nodes.pop(n)
        self.arguments.pop(n)

    def setline(self, n, line):
        """
        set the netlist line 'n' whith provided dictionary
        """
        value = line['dictionary']
        try:
            value = ast.literal_eval(value)
        except ValueError:
            pass
        self.dictionaries[n] = value

        value = line['component']
        try:
            value = ast.literal_eval(value)
        except ValueError:
            pass
        self.components[n] = value

        value = line['label']
        try:
            value = ast.literal_eval(value)
        except (ValueError, SyntaxError):
            pass
        self.labels[n] = value

        value = line['nodes']
        self.nodes[n] = value

        value = line['arguments']
        self.arguments[n] = value

    def to_graph(self, label=None):
        """
        Return the graph associated with the netlist.

        Parameter
        ---------

        label : str (optional)
            String label for the returned graph object.

        Output
        ------

        graph : pyphs.Graph
            The graph object associated with the netlist.
        """
        from .graph import Graph
        return Graph(netlist=self, label=label)

    def to_core(self, label=None):
        """
        Return the graph associated with the netlist.

        Parameter
        ---------

        label : str (optional)
            String label for the returned graph object.

        Output
        ------

        graph : pyphs.Core
            The PHS core object associated with the netlist.
        """
        graph = self.to_graph(label=label)
        return graph.to_core(label=label)

    def to_method(self, label=None, config=None):
        """
        Return the PHS numerical method associated with the PHS graph for the
        specified configuration.

        Parameter
        ---------

        label : str (optional)
            String label for the Core object (default None recovers the label
            from the graph).

        config : dict or None
            A dictionary of simulation parameters. If None, the standard
            pyphs.config.simulations is used (the default is None).
            keys and default values are

              'fs': 48e3,           # Sample rate (Hz)
              'grad': 'discret',    # In {'discret', 'theta', 'trapez'}
              'theta': 0.,          # Theta-scheme for the structure
              'split': False,       # split implicit from explicit part
              'maxit': 10,          # Max number of iterations for NL solvers
              'eps': 1e-16,         # Global numerical tolerance

        Output
        ------

        method : pyphs.Method
            The PHS numerical method associated with the PHS graph for the
            specified configuration.
        """

        core = self.to_core(label=label)
        return core.to_method(config=config)

    def to_simulation(self, label=None, config=None, inits=None, erase=True):
        """
        Return the PHS simulation object associated with the PHS netlist for the
        specified configuration.

        Parameter
        ---------

        label : str (optional)
            String label for the Core object (default None recovers the label
            from the graph).

        config : dict or None
            A dictionary of simulation parameters. If None, the standard
            pyphs.config.simulations is used (the default is None).
            keys and default values are

              'fs': 48e3,           # Sample rate (Hz)
              'grad': 'discret',    # In {'discret', 'theta', 'trapez'}
              'theta': 0.,          # Theta-scheme for the structure
              'split': False,       # split implicit from explicit part
              'maxit': 10,          # Max number of iterations for NL solvers
              'eps': 1e-16,         # Global numerical tolerance

        erase : bool (optional)
            If True and a h5file exists with same path than simulation data,
            it is erased. Else, it is used to initialize the data object. The
            default is True.

        Output
        ------

        method : pyphs.Simulation
            The PHS simulation object associated with the PHS netlist for the
            specified configuration.
        """

        core = self.to_core(label=label)
        return core.to_simulation(config=config, inits=inits, erase=erase)

def print_netlist_line(dic):
    """
    Return the line of the pyphs netlist associated to
    > dic.comp label nodes parameters

    Parameters
    ----------

    item : dict

        Dictionary that encodes the component with keys:

            * 'dictionary': str

                module in 'pyphs/dicitonary/'

            * 'component':

                component in 'dictionary'

            * 'label':

                component label

            * 'nodes':

                tuple of nodes identifiers

            * 'arguments': dict

                Dictionary of parameters. Keys are parameters labels in \
dic.comp, and values are float (parameter value), str (new parameter label) \
or tuple (str, float).

    Output
    -------

    line : str

        Formated string that corresponds to a single line in the netlist \
        (includes end cariage return).
    """

    component = '{0}.{1} {2} {3}:'.format(dic['dictionary'],
                                          dic['component'],
                                          dic['label'],
                                          dic['nodes'])
    pars = ""
    if dic['arguments'] is not None:
        for par in dic['arguments'].keys():
            pars += ' {}={};'.format(par, str(dic['arguments'][par]))
    line = component + pars + '\n'
    return line
