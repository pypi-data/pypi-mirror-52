#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 28 11:52:47 2019

@author: hogbobson
"""
import numpy as np

from . import force


def distances(vec): # There must be an easier way.
    """ Converts matrix elements from origin -> object to object -> object. \
    Naturally, the dimensions in the matrix increase because of that. """
    newr = np.zeros((np.shape(vec)[0],np.shape(vec)[0],3))
    for i in range(3):  #For future: get rid of loop, if possible.
        newr[:,:,i] = vec[:,i].reshape(1,np.size(vec[:,i])) - \
        vec[:,i].reshape(np.size(vec[:,i]),1)
    return newr 

def get_force_variables(forces):
    LOFK = [] # List of Force Keys
    if force.gravity in forces:
        LOFK.append('mass')
    #if force.lennard_jones in forces:
    #    LOFK.append('LJ-constants')
    if force.electrostatics in forces:
        LOFK.append('charge')
    return LOFK


def legit_body_parametres(input_key):
    allowed_keys = ['charge']
    if input_key not in allowed_keys:
        raise(input_key + ' is not a valid parameter!')
    

def ensemble_checker(ensemble, force_vars):
    proto_ensemble = {'position'        : [type(np.empty(0))],
                      'position magnitude' : [type(np.empty(0))],
                      'position data'   : [type(np.empty(0))],
                      'distance'        : [type(np.empty(0))],
                      'velocity'        : [type(np.empty(0))],
                      'velocity magnitude': [type(np.empty(0))],
                      'mass'            : [type(np.empty(0))],
                      'energy'          : [type(None)],
                      'energy data'     : [type(None)],
                      'number of objects': [type(1), type(1.)],
                      'label'           : [type([])],
            }
    
    for key, type_at_key in proto_ensemble.items():
        try:
            if type(ensemble[key]) in type_at_key:
                print('key: ' + key + ' has a correct type')
            else:
                raise SystemExit('The ensemble at key: ' + key + ' has type' + \
                       str(type(ensemble[key])) + ', expected type ' + \
                       type_at_key)
        except KeyError:
            raise('Ensemble has no key' + key)
    
    # TODO: MAKE BELOW WORK
# =============================================================================
#     req_force_keys = {}
#     for key in force_vars:
#         req_force_keys[key] = [type(np.empty(0))]
#     
#     for key, type_at_key in req_force_keys.items():
#         try:
#             if type(ensemble[key]) in type_at_key:
#                 print('key: ' + key + ' has a correct type')
#             else:
#                 raise SystemExit('The ensemble at key: ' + key + ' has type' + \
#                        str(type(ensemble[key])) + ', expected type ' + \
#                        type_at_key)
#         except KeyError:
#             raise('Ensemble has no key' + key)
# =============================================================================
    


# =============================================================================
# def sym_kick(ensemble, dt, d, forces):#, acceleration):
#     ensemble['velocity'] += d * dt * acceleration(ensemble, forces)
#     return ensemble
# 
# def sym_drift(ensemble, dt, c):
#     ensemble['r'] += c * dt * ensemble['velocity']
#     ensemble['distance'] = distances(ensemble['r'])
#     return ensemble
# 
# def acceleration(ensemble, forces):
#     acc = np.zeros_like(ensemble['r'])
#     for force_func in forces:
#         acc += force_func(ensemble['distance'], ensemble['mass'])
#     return acc
# =============================================================================
    