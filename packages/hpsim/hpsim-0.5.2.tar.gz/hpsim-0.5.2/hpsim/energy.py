#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 14:38:23 2019

@author: hogbobson
"""
import numpy as np

def no_energy(ensemble):
    pass

def brute_kinetic_energy(ensemble):
    n = ensemble['number of objects']
    ensemble['energy'] = 0.5 * ensemble['mass'] * \
            ensemble['velocity magnitude'] * ensemble['velocity magnitude']
    ensemble['energy data'] = np.append(ensemble['energy data'], \
            np.reshape(ensemble['energy'], (n ,1)), axis = 1)
    return ensemble
    