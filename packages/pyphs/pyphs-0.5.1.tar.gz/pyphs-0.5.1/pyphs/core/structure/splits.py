#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May 15 15:14:37 2017

@author: Falaize
"""

from .moves import (movematrixcols, movesquarematrixcolnrow,
                    move_stor, move_diss)
from ..tools import free_symbols
from ..maths import hessian, jacobian, gradient, matvecprod
import sympy


def monovar_multivar(core):
    """
    Split core components into monovariate and multivariate components.
    """

    # split storage part
    i = 0
    for _ in range(core.dims.x()):
        hess = hessian(core.H, core.x)
        hess_line = list(hess[i, :].T)
        # remove i-th element
        hess_line.pop(i)
        # if other elements are all 0
        if all(el is sympy.sympify(0) for el in hess_line):
            # do nothing and increment counter
            i += 1
        else:
            # move the element at the end of states vector
            move_stor(core, i, core.dims.x())
    # number of separate components
    core.dims.xs = i
    # number of non-separate components
    core.dims.xns = core.dims.x()-i
    # split dissipative part
    i = 0
    for _ in range(core.dims.w()):
        Jacz_line = list(core.Jacz[i, :].T)
        # remove i-th element
        Jacz_line.pop(i)
        # if other elements are all 0
        if all(el is sympy.sympify(0) for el in Jacz_line):
            # do nothing and increment counter
            i += 1
        else:
            # move the element at the end of variables vector
            move_diss(core, i, core.dims.w())
    # number of separate components
    core.dims.ws = i
    # number of non-separate components
    core.dims.wns = core.dims.w()-i


# ============================== linear_nonlinear =========================== #
def linear_nonlinear(core, criterion=None):
    """
    1. Detect the number of linear storage component (_nxl) and of linear
    dissipative components (_nwl).
    2. Sort components as [linear, nonlinear].
    3. Build matrices Q, bl and Zl such as
       H_l(x_l) = 1/2 x_l^T.Q.x_l + x_l^T.bl
       Z_l(w_l) = Zl.wl

    Parameters
    ----------

    core : pyphs.Core
        Core to analyse.

    criterion: list of tuples of objects or None (optional)
        criterion[0] = (hessH, argx)
        criterion[1] = (jacz,  argz)
    """
    if criterion is None:
        args = (core.x + core.dx() + core.w, core.dx() + core.w)
        mats = (hessian(core.H, core.x), jacobian(core.z, core.w))
        criterion = list(zip(mats, args))
        movefunc = movesquarematrixcolnrow
    else:
        movefunc = movematrixcols

    # split storage part
    nxl = 0
    hess = criterion[0][0]
    arg = criterion[0][1]
    for _ in range(hess.shape[1]):
        # hess_row = list(hess[nxl, :].T)
        hess_col = list(hess[:, nxl])
        # collect line symbols
        symbs = free_symbols(hess_col)
        # if symbols are not states
        if symbs.isdisjoint(arg):
            # do nothing and increment counter
            nxl += 1
        else:
            # move the element at the end of states vector
            move_stor(core, nxl, core.dims.x()-1)
            hess = movefunc(hess, nxl, core.dims.x()-1)

    # split dissipative part
    nwl = 0
    jacz = criterion[1][0]
    arg = criterion[1][1]
    for _ in range(jacz.shape[1]):
        # jacz_row = list(jacz[nwl, :].T)
        jacz_col = list(jacz[:, nwl])
        # collect line symbols
        symbs = free_symbols(jacz_col)
        # if symbols are not dissipation variables
        if symbs.isdisjoint(arg):
            # do nothing and increment counter
            nwl += 1
        else:
            # move the element to end of dissipation variables vector
            move_diss(core, nwl, core.dims.w()-1)
            jacz = movefunc(jacz, nwl, core.dims.w()-1)

    # number of linear components
    setattr(core.dims, '_xl', nxl)
    # Hamiltonian of linear components
    # Quadratic part
    Q = hessian(core.H, core.xl())
    # Linear part
    bl = [a-b for a, b in zip(gradient(core.H, core.xl()), matvecprod(Q, core.xl()))]

    core.setexpr('Q', Q)
    core.setexpr('bl', bl)

    # number of linear components
    setattr(core.dims, '_wl', nwl)
    core.setexpr('Zl', jacobian(core.zl(), core.wl()))
