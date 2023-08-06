#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 11:18:52 2019

@author: hogbobson
"""

import h5py
from matplotlib import pyplot as plt
from matplotlib import animation

def mkfile(data, name):
    f = h5py.File(name + '.hd5f', 'w')
    f.create_dataset(name, data = data)
    f.close()