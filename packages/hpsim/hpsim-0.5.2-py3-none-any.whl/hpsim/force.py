#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
force.py is supposed to contain all of the pre-defined forces you can use.
You can make your own, of course, but it's good to have several.
"""
# External modules
import numpy as np
from numpy import linalg as LA
from scipy import constants as cnst

# Internal modules
from hpsim.miscfuncs import distances

def gravity(pos, mass):
    """ gravity calculates - you guessed it - gravity. It works with the now
    300-year-old equation F = GMm/r². """
    
    print(type(mass))
    
    dist = distances(pos)               # Find distances between objects
    dist_mag = LA.norm(dist, axis = 2)  # And the magnitude of these distances
    dist_mag[dist_mag == 0] = np.nan    # We'll divide soon - 0s not allowed
    dist_cub = dist_mag*dist_mag*dist_mag # r^3
    F_all = cnst.gravitational_constant * mass.reshape((1, len(mass), 1)) * \
            mass.reshape((len(mass), 1, 1)) * dist / \
            dist_cub.reshape(np.append(np.shape(dist_mag), 1))
    F_all[np.isnan(F_all)] = 0    
    F = np.sum(F_all, axis = 1)
    return F


def electrostatics(pos, charge):
    """ electrostatics calculates electrostatic forces between charged
    particles, using F = 1/(4\pi\eps_0)*qQ/r² """
    
    charge = np.array(charge)    
    dist = distances(pos)               # Find distances between objects
    dist_mag = LA.norm(dist, axis = 2)  # And the magnitude of these distances
    dist_mag[dist_mag == 0] = np.nan    # We'll divide soon - 0s not allowed
    dist_cub = dist_mag*dist_mag*dist_mag # r^3
    F_all = 1/(4*np.pi*cnst.epsilon_0) * charge.reshape((1, len(charge), 1)) * \
            charge.reshape((len(charge), 1, 1)) * dist / \
            dist_cub.reshape(np.append(np.shape(dist_mag), 1))
    F_all[np.isnan(F_all)] = 0
    F = np.sum(F_all, axis = 1)
    return F

# TODO: LENNARD JONES
# TODO: SIMPLE SURFACE GRAVITY
    
def check_force(force_to_check):
    # TODO: MAKE more GENERAL
    gravity_return = {'keys': ['force gravity', 'args gravity'],
                      'arg_keys': ('position', 'mass')}
    electrostatics_return = {'keys': ['force electrostatics', 
                                      'args electrostatics'],
                      'arg_keys': ('position', 'charge')}
    
    if force_to_check == gravity:
        return gravity_return
    elif force_to_check == electrostatics:
        return electrostatics_return
    else:
        return False