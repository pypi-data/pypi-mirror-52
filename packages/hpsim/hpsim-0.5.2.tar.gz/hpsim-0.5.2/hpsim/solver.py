#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
solver.py contains everything related to solvers, that is, integrators... they
make time move forward, okay!
"""


def sym1(ensemble, dt):
    ensemble = sym_kick(ensemble, dt, 1)
    ensemble = sym_drift(ensemble, dt, 1)
    return ensemble


def sym2(ensemble, dt):
    ensemble = sym_kick(ensemble, dt, 0.5)
    ensemble = sym_drift(ensemble, dt, 1)
    ensemble = sym_kick(ensemble, dt, 0.5)
    return ensemble

# TODO: SYM3
# TODO: SYM4
# TODO: RK





def sym_kick(ensemble, dt, d):
    ensemble['velocity'] += d * dt * ensemble['acceleration']
    return ensemble


def sym_drift(ensemble, dt, c):
    ensemble['position'] += c * dt * ensemble['velocity']
    return ensemble





