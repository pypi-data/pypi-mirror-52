#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 17:04:09 2019

@author: hogbobson
"""

import numpy as np
from numpy import random as rng, linalg as LA
from astropy import constants as astcnst
from math import radians as rad
from hpsim import energy
from hpsim.miscfuncs import distances
from hpsim.miscfuncs import legit_body_parametres as lbp
from hpsim.timegen import current_time

class StarSystemGenerator:
    def __init__(self):
        self.r      = np.empty((0,3), float)    # Position r
        self.v      = np.empty((0,3), float)    # Velocity v
        self.m      = []                        # Mass m
        self.n      = 0                         # Number of objects
        self.label  = []                        # Label, for ???
        self.set_time()#td = {'year': 1990, 'month': 4, 'day': 19, 'hour': 0})
        #self.central_star()
        
    
    def _rotation_x(self, phi):
        R = np.zeros((3,3))
        R[0,0] = 1
        R[1,1] = np.cos(phi)
        R[1,2] = -np.sin(phi)
        R[2,1] = np.sin(phi)
        R[2,2] = np.cos(phi)
        return R
    
    
    def _rotation_z(self, phi):
        R = np.zeros((3,3))
        R[0,0] = np.cos(phi)
        R[1,1] = np.cos(phi)
        R[0,1] = -np.sin(phi)
        R[1,0] = np.sin(phi)
        R[2,2] = 1
        return R
        
    
    def _ecc_anomaly(self, E0, e, M):
        E1 = E0 - (E0 - e*np.sin(E0) - M)/(1 - e*np.cos(E0))
        if E1 - E0 > 1e-5:# and E1 < E0:
            return self._ecc_anomaly(E1, e, M)
        elif E1 - E0 < 1e5:# and E1 < E0:
            return E1
        #elif E1 > E0:
        #    raise Exception('orbit is not elliptical')
        
        
    def _orbit_to_cart(self, Omega, i, omega, a, e, M):
        # Get shorter constants        
        G = astcnst.G.value
        M_sun = self.m[0]
        eps = rad(23.43928)
        
        # Calculations
        E       = self._ecc_anomaly(M, e, M)
        nu      = 2*np.arctan2(np.sqrt(1+e)*np.sin(E/2), \
                               np.sqrt(1-e)*np.cos(E/2))
        rm      = a * (1 - e*np.cos(E))
        o       = rm * np.array([np.cos(nu), np.sin(nu), 0])
        odot    = np.sqrt(G * M_sun * a) / rm * \
                       np.array([-np.sin(E), np.sqrt(1 - e*e)*np.cos(E), 0])
                       
        # Rotation matrices
        R_z_O   = self._rotation_z(-Omega)
        R_x_i   = self._rotation_x(-i)
        R_z_o   = self._rotation_z(-omega)
        
        # Outputs
        r       = np.dot(R_z_O, np.dot(R_x_i, np.dot(R_z_o, o)))
        v       = np.dot(R_z_O, np.dot(R_x_i, np.dot(R_z_o, odot)))
        #r = o
        #v = odot
        
        # MAYBE MOVE THIS PART OUT EVENTUALLY
        #r[1]    = np.cos(eps)*r[1] - np.sin(eps)*r[2]
        #r[2]    = np.sin(eps)*r[1] + np.cos(eps)*r[2]
        #v[1]    = np.cos(eps)*v[1] - np.sin(eps)*v[2]
        #v[2]    = np.sin(eps)*v[1] + np.cos(eps)*v[2]
        
        # Appending
        self.r = np.append(self.r, np.array([r]), axis = 0)
        self.v = np.append(self.v, np.array([v]), axis = 0)
        self.n += 1        
    
    
    
    def get_ensemble(self):
        ensemble = {'r'             : self.r                                ,
                    'r magnitude'   : LA.norm(self.r, axis = 1)             ,
                    'r data'        : np.reshape(self.r, (self.n, 3, 1))    ,
                    'distance'      : distances(self.r)                     ,
                    'velocity'      : self.v                                ,
                    'velocity magnitude': LA.norm(self.v, axis = 1)         ,
                    'mass'          : self.m                                ,
                    'energy'        : None                                  ,
                    'energy data'   : None                                  ,
                    'number of objects': self.n                             ,
                    'label'         : self.label                            ,
                    'remaining'     : None
                }
        return ensemble
    
    def set_ensemble(self):
        pass
    
    def set_time(self, td = current_time()):
        """ Function setting the day-number as per section 3 at
            https://stjarnhimlen.se/comp/ppcomp.html """
        y = td['year']
        m = td['month']
        D = td['day']
        UT = td['hour']
        self.day_number = 367*y - 7 * ( y + (m+9)//12 ) // 4 - \
                        3 * ( ( y + (m-9)//7 ) // 100 + 1 ) // 4 + \
                        275*m//9 + D - 730515 + UT/24.0
    
    
    
    def rev(self, angle):
        while angle > np.pi:
            angle -= 2*np.pi
        while angle < -np.pi:
            angle += 2*np.pi
        return angle
    
    
    def mean_anomaly(self, semi_major_axis, M_central = astcnst.M_sun.value):
        pass
        
    
    def central_star(self, mass = astcnst.M_sun.value):
        self.r = np.append(self.r, [[0., 0., 0.,]], axis = 0)
        self.v = np.append(self.v, [[0., 0., 0.,]], axis = 0)
        self.m = np.append(self.m, mass)
        self.label.append('Sun')
        self.n += 1
        
    
    
    # Omega     = Longitude of the Ascending Node (LAN) [rad]
    # i         = Inclination [rad]
    # omega     = Argument of Periapsis [rad]
    # a         = Semi-major-axis [m]
    # e         = Eccentricity [1]
    # M         = Mean anomaly [rad]
    # Thank you to https://stjarnhimlen.se/comp/ppcomp.html
    
    def mercury(self):
        # Get shorter constants
        d = self.day_number
        
        # Inputs
        Omega   = self.rev(rad(48.3313 + 3.24587E-5 * d))
        i       = self.rev(rad(7.0047 + 5.00E-8 * d))
        omega   = self.rev(rad(29.1241 + 1.01444E-5 * d))
        a       = 0.387098*astcnst.au.value
        e       = 0.205635 + 5.59E-10 * d
        M       = self.rev(rad(168.6562 + 4.0923344368 * d))
        
        self._orbit_to_cart(Omega, i, omega, a, e, M)
        self.label.append('Mercury')
        self.m  = np.append(self.m, astcnst.M_earth.value*0.0553)
    
    def venus(self):
        # Get shorter constants
        d = self.day_number
        
        # Inputs
        Omega   = self.rev(rad(76.6799 + 2.46590E-5 * d))
        i       = self.rev(rad(3.3946 + 2.75E-8 * d))
        omega   = self.rev(rad(54.8910 + 1.38374E-5 * d))
        a       = 0.723330*astcnst.au.value
        e       = 0.006773 - 1.302E-9 * d
        M       = self.rev(rad(48.0052 + 1.6021302244 * d))
        
        self._orbit_to_cart(Omega, i, omega, a, e, M)
        self.label.append('Venus')
        self.m  = np.append(self.m, astcnst.M_earth.value*0.815)
    
    def earth(self):
        # Get shorter constants
        d = self.day_number
        
        # Inputs
        Omega   = 0.
        i       = 0.
        omega   = self.rev(rad(282.9404 + 4.70935e-5 * d))
        a       = astcnst.au.value
        e       = 0.016709 - 1.151E-9 * d
        M       = self.rev(rad(356.0470 + 0.9856002585 * d))
        
        self._orbit_to_cart(Omega, i, omega, a, e, M)
        self.label.append('Earth')
        self.m  = np.append(self.m, astcnst.M_earth.value)
        
    
    def mars(self):
        # Get shorter constants
        d = self.day_number
        
        # Inputs
        Omega   = self.rev(rad(49.5574 + 2.11081E-5 * d))
        i       = self.rev(rad(1.8497 - 1.78E-8 * d))
        omega   = self.rev(rad(286.5016 + 2.92961E-5 * d))
        a       = 1.523688*astcnst.au.value
        e       = 0.093405 + 2.516E-9 * d
        M       = self.rev(rad(18.6021 + 0.5240207766 * d))
        
        self._orbit_to_cart(Omega, i, omega, a, e, M)
        self.label.append('Mars')
        self.m  = np.append(self.m, astcnst.M_earth.value*0.107)
    
    def jupiter(self):
        # Get shorter constants
        d = self.day_number
        
        # Inputs
        Omega   = self.rev(rad(100.4542 + 2.76854e-5 * d))
        i       = self.rev(rad(1.3030 - 1.557e-7 * d))
        omega   = self.rev(rad(273.8777 + 1.64505E-5 * d))
        a       = 5.20256*astcnst.au.value
        e       = 0.048498 + 4.469E-9 * d
        M       = self.rev(rad(19.8950 + 0.0830853001 * d))
        
        self._orbit_to_cart(Omega, i, omega, a, e, M)
        self.label.append('Jupiter')
        self.m  = np.append(self.m, astcnst.M_jup.value)
        
        
    def saturn(self):
        # Get shorter constants
        d = self.day_number
        
        # Inputs
        Omega   = self.rev(rad(113.6634 + 2.38980E-5 * d))
        i       = self.rev(rad(2.4886 - 1.081E-7 * d))
        omega   = self.rev(rad(339.3939 + 2.97661E-5 * d))
        a       = 9.55475*astcnst.au.value
        e       = 0.055546 - 9.499E-9 * d
        M       = self.rev(rad(316.9670 + 0.0334442282 * d))
        
        self._orbit_to_cart(Omega, i, omega, a, e, M)
        self.label.append('Saturn')
        self.m  = np.append(self.m, astcnst.M_earth.value * 95.16)
    
    def uranus(self):
        # Get shorter constants
        d = self.day_number
        
        # Inputs
        Omega   = self.rev(rad(74.0005 + 1.3978E-5 * d))
        i       = self.rev(rad(0.7733 + 1.9E-8 * d))
        omega   = self.rev(rad(96.6612 + 3.0565E-5 * d))
        a       = 19.18171 - 1.55E-8 * d * astcnst.au.value
        e       = 0.047318 + 7.45E-9 * d
        M       = self.rev(rad(142.5905 + 0.011725806 * d))
        
        self._orbit_to_cart(Omega, i, omega, a, e, M)
        self.label.append('Uranus')
        self.m  = np.append(self.m, astcnst.M_earth.value * 14.54)
    
    def neptune(self):
        # Get shorter constants
        d = self.day_number
        
        # Inputs
        Omega   = self.rev(rad(131.7806 + 3.0173E-5 * d))
        i       = self.rev(rad(1.7700 - 2.55E-7 * d))
        omega   = self.rev(rad(272.8461 - 6.027E-6 * d))
        a       = 30.05826 + 3.313E-8 * d * astcnst.au.value
        e       = 0.008606 + 2.15E-9 * d
        M       = self.rev(rad(260.2471 + 0.005995147 * d))
        
        self._orbit_to_cart(Omega, i, omega, a, e, M)
        self.label.append('Neptune')
        self.m  = np.append(self.m, astcnst.M_earth.value * 17.15)
        
    def all_known_planets(self):
        self.mercury()
        self.venus()
        self.earth()
        self.mars()
        self.jupiter()
        self.saturn()
        #self.uranus()
        #self.neptune()
    
    def random_planets(self, num = 5):
        def log_uniform(low, high, size = 1, base = 10):
            return np.power(base, rng.uniform(low, high, size))
        
        for i in range(num):
            Omega = 360*rng.random() - 180
            i     = np.pi/6*rng.randn()
            omega = 360*rng.random() - 180
            a     = log_uniform(-2, 1) * astcnst.au.value
            e     = np.minimum(np.abs(rng.randn()*0.1), 0.95)
            M     = 360*rng.random() - 180
            
            self._orbit_to_cart(Omega, i, omega, a, e, M)
            self.label.append(['planet #', i])
            self.m = np.append(self.m, np.maximum(rng.randn()+3, 1e-5) \
                               * astcnst.M_earth.value*1e-3)
    

class many_bodies_generator:
    def __init__(self, scale = 'molecular', 
                 charge_init_and_spread = [None, None],):
        
        self.r      = np.empty((0,3), float)    # Position r
        self.v      = np.empty((0,3), float)    # Velocity v
        self.m      = []                        # Mass m
        self.n      = 0                         # Number of objects
        self.label  = []                        # Label, for ???
        self.parameter_dict = {}
        # TODO: MAKE IT AN OPTION TO MAKE YOUR OWN PHYSICAL PARAMETRES,
        # INSTEAD OF JUST CHANING THE VALUES OF THE PARAMETRES I HAVE DEFINED.
        if None not in charge_init_and_spread:
            self.q  = []
            self.parameter_dict['var charge'] = self.q
            self.parameter_dict['init charge'] = charge_init_and_spread[0]
            self.parameter_dict['spread charge'] = charge_init_and_spread[1]
        else:
            self.q  = None
        
    
    def make_body(self, offset = np.zeros((1,3)), 
                  initial_velocity = np.zeros((1,3)),
                  initial_mass = 1,
                  spread_pos = 10,
                  spread_vel = 0,
                  spread_mass = 0):
        """ Makes a body based on input parametres and the parametres
        initialised in the instance of many_bodies_generator. """
        def log_uniform(low, high, size = 1, base = 10):
            return np.power(base, rng.uniform(low, high, size))
        
        pos = spread_pos * rng.randn(3) + offset
        vel = spread_vel * rng.randn(3) + initial_velocity
        mass = np.abs(spread_mass * rng.randn(1)) + initial_mass
        
        # Setting up setting up the secial parametres
        par_keys = list(self.parameter_dict.keys())
        for i in np.arange(0, len(par_keys), 3):
            self.parameter_dict[par_keys[i]][:] = \
                np.append(self.parameter_dict[par_keys[i]][:],
                          self.parameter_dict[par_keys[i+2]] * rng.randn(1) +
                          self.parameter_dict[par_keys[i+1]])
        self.r = np.append(self.r, pos, axis = 0)
        self.v = np.append(self.v, vel, axis = 0)
        self.m = np.append(self.m, mass)
        self.n += 1
        
    
    def make_many_bodies(self, num_bods, offset = 0, 
                  initial_velocity = 0,
                  initial_mass = 1,
                  spread_pos = 10,
                  spread_vel = 0,
                  spread_mass = 0):
        """ Makes a body based on input parametres and the parametres
        initialised in the instance of many_bodies_generator. """
        def log_uniform(low, high, size = 1, base = 10):
            return np.power(base, rng.uniform(low, high, size))
        
        pos = spread_pos * rng.randn((num_bods, 3)) + offset
        vel = spread_vel * rng.randn((num_bods, 3)) + initial_velocity
        mass = np.abs(spread_mass * rng.randn(num_bods)) + initial_mass
        
        # Setting up setting up the secial parametres
        par_keys = list(self.parameter_dict.keys())
        for i in np.arange(0, len(par_keys), 3):
            self.parameter_dict[par_keys[i]][:] = \
                np.append(self.parameter_dict[par_keys[i]][:],
                          self.parameter_dict[par_keys[i+2]] * \
                          rng.randn(num_bods) +
                          self.parameter_dict[par_keys[i+1]])
        self.r = np.append(self.r, pos, axis = 0)
        self.v = np.append(self.v, vel, axis = 0)
        self.m = np.append(self.m, mass)
        self.n += num_bods
        
    
    
    def get_ensemble(self):
        ensemble = {'position'      : self.r,
                    'position magnitude': LA.norm(self.r, axis = 1),
                    'position data' : np.reshape(self.r, (self.n, 3, 1)),
                    'distance'      : distances(self.r),
                    'velocity'      : self.v,
                    'velocity magnitude': LA.norm(self.v, axis = 1),
                    'mass'          : self.m,
                    'energy'        : None,
                    'energy data'   : None,
                    'number of objects': self.n,
                    'label'         : self.label,
                    'remaining'     : None,
                    'charge'        : self.q
                }
        return ensemble
        
        
    
    
def solar_system():
    SSG = StarSystemGenerator()
    SSG.central_star()
    SSG.all_known_planets()
    
    ensemble = SSG.get_ensemble()
    #ensemble = energy.brute_kinetic_energy(ensemble)
    return ensemble
    
def random_solar_system():
    SSG = StarSystemGenerator()
    SSG.central_star()
    SSG.random_planets(5)
    #SSG.velocities_with_central_star()
    
    ensemble = SSG.get_ensemble()
    #ensemble = energy.brute_kinetic_energy(ensemble)
    return ensemble
        
def no_central_object(num_bodies = 10):
    MBG = many_bodies_generator(charge_init_and_spread = [1, 0])
    for i in range(num_bodies):
        MBG.make_body()
    return MBG.get_ensemble()
        