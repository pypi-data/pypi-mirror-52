#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 28 19:46:43 2019

@author: hogbobson
"""

import numpy as np
import h5py
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib import pyplot as plt
from matplotlib import animation

    
def no_plot(everything):
    return None


def standard_plot(everything):
    ensemble = everything['ensemble']
    n = ensemble['number of objects']
    plt.figure(num = 0, figsize = (8,8))
    for i in range(n):
        plt.plot(ensemble['position data'][i,0,:], 
                 ensemble['position data'][i,1,:], '-',
                 label = ensemble['label'][i],
                 color = (abs(np.sin(i)), 0 + i/n, 1-i/n))
    plt.xlabel('x')
    plt.ylabel('y')
    xlim = np.max(ensemble['position data'])*1.1
    #xlim = 5*1e11
    plt.axis((-xlim, xlim, -xlim, xlim))
    plt.legend()
    plt.show()
    return None


def mkfile(data, name):
    fname = name + '.hdf5'
    f = h5py.File(fname, 'w')
    f.create_dataset(name, data = data)
    f.close()
    

def simple_2d_anim(ensemble, stps):
    data = ensemble['position data']
    nobjs = ensemble['number of objects']
    nsteps = stps
    labels = ensemble['label']
    
    fig, ax = plt.subplots(figsize = (8,8))
    lim = np.max(data)*1.2
    if lim > 1e13:
        lim = 5e11
    
    x = data[:,0,:]
    y = data[:,1,:]
    
    x_start = data[:,0,0]
    y_start = data[:,1,0]
    
    if labels:
        lines = [ax.plot(x_start[j], y_start[j], 'o', label = labels[j])[0] \
             for j in range(int(nobjs))]
    else:
        lines = [ax.plot(x_start[j], y_start[j], 'o')[0] \
             for j in range(int(nobjs))]
    
    ax.set_xlim([-lim, lim])
    ax.set_xlabel('x [m]')
    ax.set_ylim([-lim, lim])
    ax.set_ylabel('y [m]')
    ax.legend()
    
    
    def animate(i, x, y, lines):
        for line, p in zip(lines, range(int(nobjs))):
            line.set_xdata(x[p,i])
            line.set_ydata(y[p,i])
        return lines
    
    
    
    ani = animation.FuncAnimation(fig, animate, np.arange(0,nsteps-1), \
                                  fargs = (x, y, lines), \
                                  interval = 10)
    
    plt.draw()
    
    #ani.save('yolo.MPEG', writer = 'ffmpeg')
    return ani
    
def simple_3d_anim(everything):
    def update_points(num, dataLines, ax):
        ax.clear()
        ax.scatter(
                dataLines[0][0][num],
                dataLines[0][1][num],
                dataLines[0][2][num],
                s=100,
                marker='o',
                c='yellow'
                )
        
        ax.scatter(
                dataLines[1:][0][num],
                dataLines[1:][1][num],
                dataLines[1:][2][num],
                s=5,
                marker='o',
                c='blue'
                )
        
        

    # Attaching 3D axis to the figure
    fig = plt.figure()
    ax = p3.Axes3D(fig)
    
    
    data = everything['ensemble']['r data']
    numobjs = everything['ensemble']['number of objects']
    numstps = everything['time steps']
    
    datalines = [data[i] for i in range(int(numobjs))]
    print(np.shape(datalines))
    
    
    
    lim = np.max(data)
    # Setting the axes properties
    ax.set_xlim3d([-lim, lim])
    ax.set_xlabel('X')
    
    ax.set_ylim3d([-lim, lim])
    ax.set_ylabel('Y')
    
    ax.set_zlim3d([-lim, lim])
    ax.set_zlabel('Z')
    
    ax.set_title('3D Test')
    
    # Creating the Animation object
    line_ani = animation.FuncAnimation(fig, update_points, numstps, \
                                       fargs=(datalines, ax), \
                                       interval=25, blit=False)
    plt.draw()
    
    
    
    return line_ani