#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 18:51:19 2019

@author: hogbobson
"""

import numpy as np
from . import acceleration
from . import force
from . import miscfuncs
from . import solver
from . import integrator
from . import ensgen
from . import timestep
from . import timegen
from . import visual
from . import energy

class hpsim:
    def __init__(cls):
        # The following N class variables are the main information
        # needed to run the program.
        
        cls._wanted_forces      = [force.gravity, force.electrostatics]
        cls._force_dict         = {}
        
        cls._plot_save          = False
        cls._energy_func        = energy.no_energy
        cls.time_start          = 0
        cls.time_step           = timestep.constant_dt(1)
        cls.time_end            = timegen.time_seconds(20)
        cls._time_now            = cls.time_start
        cls._iteration_steps     = 0
        
        # The next variable is derived from cls._wanted_forces, used for
        # ensemble generation.
        cls._force_variables = miscfuncs.get_force_variables(
                                            cls._wanted_forces)
        
        cls.ensemble = []
        cls.set_acceleration_function(acceleration.classic_acceleration)
        cls.set_wanted_forces(cls._wanted_forces)
        cls.set_ensemble_generator(ensgen.no_central_object)
        cls.set_integrator(integrator.n_squared)
        cls.set_solver(solver.sym2, (cls.time_step,))
        cls.set_ensemble()
        
        
        # Nothing has been tested, and the class must know!
        cls._ensemble_is_ok = False
    
    
    def set_acceleration_function(cls, func, fargs = None):
        # If no fargs are present, the input args should be empty.
        if fargs:
            cls._acceleration_args = fargs
        else:
            cls._acceleration_args = ()
        cls._acceleration = func
    
    
    # Ensemble methods follow
    def set_ensemble_generator(cls, func, fargs = None, check_now = True):
        """ This method sets the ensemble generator.
        Inputs:
        func:       
            A required input function taking any number of arguments.
            Should return the desired ensemble.
        fargs = None:
            A tuple containing all the arguments required by func.
            Can be left blank in case func takes no arguments.
        check_now = True:
            A boolean to tell if the program should test the ensem-
            ble generator now. Note that changing ensemble genera-
            tor will make the ensemble flagged as unchecked."""
        
        # If no fargs are present, the input args should be empty.
        if fargs:
            cls._ensemble_generator_args = fargs
        else:
            cls._ensemble_generator_args = ()
        cls._ensemble_generator = func
        cls._ensemble_is_ok = False
        if check_now:
            cls._ensemble_is_ok = miscfuncs.ensemble_checker(
                    cls._ensemble_generator(*cls._ensemble_generator_args),
                    cls._force_variables)
        #print(cls._ensemble_generator_args)
        #print(type(cls._ensemble_generator_args))
        #cls.ensemble = cls._ensemble_generator(*cls._ensemble_generator_args)
            
            
    def set_ensemble(cls):
        """ This method runs the ensemble generator and sets the
        ensemble - and then checks it if it hasn't already been. """
        
        #print(cls._ensemble_generator_args)
        #print(type(cls._ensemble_generator_args))
        cls.ensemble = cls._ensemble_generator(*cls._ensemble_generator_args)
        if not cls._ensemble_is_ok:
            cls._ensemble_is_ok = miscfuncs.ensemble_checker(cls.ensemble,
                                                        cls._force_variables)
    
    
    def set_integrator(cls, func, fargs = None):
        """ This method sets the integrator (name change pending).
        Inputs:
        func:
            A required input function taking any number of arguments.
            Should return the desired integration setup.
        fargs = None:
            A tuple containing all the arguments required by func.
            Can be left blank in case func takes no arguments. """
            
        if fargs:
            cls._integrator_args = fargs
        else:
            cls._integrator_args = ()
        cls._integrator = func
    
    
    def set_solver(cls, func, fargs = None):
        """ This method sets the solver (iterator) function.
        Inputs:
        func:
            A required input function taking any number of arguments.
            Should return the ensemble iterated one time step forward.
        fargs = None:
            A tuple containing all the arguments required by func.
            Can be left blank in case func takes no arguments. """
        
        if fargs:
            cls._solver_args = fargs
        else:
            cls._ensemble_generator_args = ()
        cls._solver = func
    
    
    def set_wanted_forces(cls, funcs):
        for f in funcs:
            standard_force_params = force.check_force(f)
            #check_force returns a dict if the force is standard, else False
            if standard_force_params:
                cls.set_force_dict(f, **standard_force_params)
            else:
                Warning('The force' + f + 'is not in the standard library. \
                        you should call main.set_force_dict yourself.')
        
    
    def set_force_dict(cls, func, keys, arg_keys):
        """ Sets the force dict. First key should be named "force <name>", 
        the second should be named "args <name>". It should throw an error,
        if they don't. """
        # TODO: MAKE FUNCTION THROW ERROR IF GIVEN KEYS DO NOT MATCH
        cls._force_dict[keys[0]] = func
        
        if arg_keys:
            cls._force_dict[keys[1]] = arg_keys
        else:
            cls._force_dict[keys[1]] = ()
        
        # A variable containing all keys in force_dict - for making use of it.
        cls.force_dict_keys = list(cls._force_dict.keys())
        
        # cls.force_dict_keys is supposed to contain
        # ['force force1', 'args force1'] etc
    
    def set_plot_routine(cls, func, fargs = None):
        if fargs:
            cls._plot_args = fargs
        else:
            cls._plot_args = ()
        cls._plot_func = func
        
    def record_data(cls, var_key, save_key):
        cls.ensemble[save_key] = np.append(cls.ensemble[save_key],
                                np.reshape(cls.ensemble[var_key],
                                          (cls.ensemble['number of objects'],
                                           3,1)), axis = 2)
    
    
    def step(cls):
        
        # First let the integrator make sure everything is in order
        cls._integrator(*cls._integrator_args)
        
        # Then make an empty force list
        cls.force = []
        # Iterate over all forces
        for k in np.arange(0, len(cls.force_dict_keys), 2):
            fargs = []
            # Get a tuple with all the variables needed for the forces
            for i in cls._force_dict[cls.force_dict_keys[k+1]]:
                fargs.append(cls.ensemble[i])
            fargs = tuple(fargs)
            force_func = cls._force_dict[cls.force_dict_keys[k]]
            cls.force.append(force_func(*fargs)) # FORCES
            
        # Calculate the acceleration
        cls.ensemble['acceleration'] = cls._acceleration(cls.ensemble['mass'],
                                                    *tuple(cls.force) +
                                                    cls._acceleration_args)
        
        # Then use the acceleration to iterate one step.
        cls._solver(cls.ensemble, *cls._solver_args)
        cls._iteration_steps += 1
        cls._time_now += cls.time_step
    
    
    def run(cls):
        while cls._time_now < cls.time_end:
            cls.step()
            cls.record_data('position', 'position data')
        cls.set_plot_routine(visual.simple_2d_anim, (cls._iteration_steps,))
        print(cls._plot_args)
        print(type(cls._plot_args))
        cls.plot_output = cls._plot_func(cls.ensemble, *cls._plot_args)














