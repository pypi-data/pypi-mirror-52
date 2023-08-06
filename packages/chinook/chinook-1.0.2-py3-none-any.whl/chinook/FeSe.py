#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 12:17:01 2017

@author: ryanday
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib as mpl
import chinook.build_lib as build_lib
import chinook.ARPES_lib as ARPES




def redo_SO(basis,lamdict):
    for bi in basis:
        bi.lam = lamdict[bi.atom]
    
    return basis

def orbital_order(mat_els,d):
    for hi in mat_els:
        if np.mod(hi.i,5)==2 and hi.i==hi.j:
            hi.H.append([0,0,0,-d])
        elif np.mod(hi.i,5)==3 and hi.i==hi.j:
            hi.H.append([0,0,0,d])
    return mat_els
            


#if __name__=="__main__":
    
    
############################ STRUCTURAL PARAMETERS ############################
a=3.7734 #FeSe
c = 5.5258
avec = np.array([[a/np.sqrt(2),a/np.sqrt(2),0.0],[-a/np.sqrt(2),a/np.sqrt(2),0.0],[0.0,0.0,c]])
Fe1,Fe2 = np.array([-a/np.sqrt(8),0,0]),np.array([a/np.sqrt(8),0,0])

G,X,M,Z,R,A = np.array([0,0,0]),np.array([0.5,0.0,0]),np.array([0.5,0.5,0]),np.array([0,0,0.5]),np.array([0.5,0,0.5]),np.array([0.5,-0.5,0.5])
Mx = np.array([0.5,-0.5,0.0])

############################ HAMILTONIAN PARAMETERS ############################

filenm = 'FeSe_o.txt'
CUT,REN,OFF,TOL=a*3,1/1.4,0.12,0.001

######################### MODEL GENERATION PARAMETERS ##########################

spin_dict = {'bool':True,
        'soc':True,
        'lam':{0:0.04},
        'order':'N',
        'dS':0.0,
        'p_up':Fe1,
        'p_dn':Fe2}



basis_dict = {'atoms':[0,0],
			'Z':{0:26},
			'orbs':[["32xy","32XY","32xz","32yz","32ZR"],["32xy","32XY","32xz","32yz","32ZR"]],
			'pos':[Fe1,Fe2],
        'spin':spin_dict}

K_dict = {'type':'F',
          'avec':avec,
          'pts':[M,G,M],#,Z,R,A,Z],
#			'pts':[np.array([-0.72044,0,0]),np.array([1.0165866,0,0])],
			'grain':200,
			'labels':['$\Gamma$','X','$M_y$','$\Gamma$','$M_x$']}


ham_dict = {'type':'txt',
			'filename':filenm,
			'cutoff':CUT,
			'renorm':REN,
			'offset':OFF,
			'tol':TOL,
			'spin':spin_dict,
         'avec':avec}

slab_dict = {'avec':avec,
      'miller':np.array([0,0,1]),
      'fine':(0,0),
      'thick':30,
      'vac':30,
      'termination':(0,0)}

######################### OPTICS EXPERIMENT PARAMETERS #########################


optics_dict = {'hv':0.36,
      'linewidth':0.01,
      'lifetime':0.02,
      'mesh':40,
      'T':10,
      'pol':np.array([1,0,0])}

######################### ARPES EXPERIMENT PARAMETERS #########################


ARPES_dict={'cube':{'X':[-0.5,0.5,300],'Y':[0.0,0.0,1],'kz':0.0,'E':[-0.5,0.05,500]},
        'SE':['poly',0.01,0.0,1],
        'hv': 37,
        'pol':np.array([0,1,0]),
        'mfp':7.0,
        'slab':False,
        'resolution':{'E':0.01,'k':0.01},
        'T':10,
        'W':4.0,
        'angle':0,
        'spin':None,
        'phase_shift':{'0-3-2-1':0.0,'0-3-2-3':np.pi*0.9}}#,
#        'rad_type':'fixed',
#        'rad_args':{'0-3-2-1':1.0,'0-3-2-3':-0.001j}}
 
################################# BUILD MODEL #################################

def build_TB():
    BD = build_lib.gen_basis(basis_dict)
    Kobj = build_lib.gen_K(K_dict)
    TB = build_lib.gen_TB(BD,ham_dict,Kobj)
    return TB


def ARPES_run(basis_dict,ham_dict,ARPES_dict,vfile):
    pars = []
    with open(vfile,'r') as fromfile:
        for line in fromfile:
            pars.append([float(ti) for ti in line.split(',')])
    fromfile.close()
#    pmax = 5
    pars = np.array(pars)
    basis_dict = build_lib.gen_basis(basis_dict)
    Imaps = np.zeros((len(pars),ARPES_dict['cube']['X'][2],ARPES_dict['cube']['E'][2]))
    Imapp = np.zeros((len(pars),ARPES_dict['cube']['X'][2],ARPES_dict['cube']['E'][2]))
    for p in list(enumerate(pars)):
        ham_dict['offset']=p[1][1]
        spin_dict['lam'][0] = p[1][0]
        basis_dict['bulk'] = redo_SO(basis_dict['bulk'],spin_dict['lam'])
        TB = build_lib.gen_TB(basis_dict,ham_dict)
        TB.mat_els = orbital_order(TB.mat_els[:],p[1][2])
        ARPES_expmt = ARPES.experiment(TB,ARPES_dict)
        ARPES_expmt.datacube(ARPES_dict)
        ARPES_dict['pol']=np.array([1,0,0])
        I,Ig = ARPES_expmt.spectral(ARPES_dict)
        Imaps[p[0]] = I[0,:,:]
        ARPES_dict['pol']=np.array([0,0.707,0.707])
        I,Ig = ARPES_expmt.spectral(ARPES_dict)
        Imapp[p[0]] = I[0,:,:]
    return pars,Imapp,Imaps
        


if __name__ == "__main__":
    TB = build_TB()
    TB.mat_els = orbital_order(TB.mat_els,0.03)
    
    TB2 = build_TB()
    TB2.mat_els = orbital_order(TB2.mat_els,-0.03)

    E1,_ = TB.solve_H()
    E2,_ = TB2.solve_H()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for ii in range(20):
        ax.plot(TB.Kobj.kcut,E1[:,ii],c='k')
        ax.plot(TB.Kobj.kcut,E2[:,ii],c='r')
        
    ax.set_xlim(TB.Kobj.kcut[0],TB.Kobj.kcut[-1])
    ax.set_ylim(-0.25,0.05)
    
    exp1 = ARPES.experiment(TB,ARPES_dict)
    exp2 = ARPES.experiment(TB2,ARPES_dict)
    
    exp1.datacube()
    exp2.datacube()
    
    I1,Ig1,_ = exp1.spectral(slice_select=('y',0),plot_bands=True)
    I2,Ig2,_ = exp2.spectral(slice_select=('y',0),plot_bands=True)
    
    fig = plt.figure()
    x = np.linspace(*ARPES_dict['cube']['X'])
    w = np.linspace(*ARPES_dict['cube']['E'])
    W,X = np.meshgrid(w,x)

    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111)

    ax2.pcolormesh(X,W,(Ig1+Ig2)[0,:,:],cmap=cm.Greys_r) 
    ax2.set_ylim(-0.25,0.05)
    plt.show()
#    experiment = ARPES.experiment(TB,ARPES_dict)
#    experiment.datacube()
#    I,Ig=  experiment.spectral(slice_select=('y',0))
    
#    spol = np.array([0,1,0])
#    ppol = np.array([.707,0,-0.707])
#    cr = spol+1.0j*ppol
#    cl = spol-1.0j*ppol
#    ARPES_dict['pol'] = spol
#    Ir,Igr = experiment.spectral(ARPES_dict,slice_select=('y',0))
#    ARPES_dict['pol'] = cl
#    Il,Igl = experiment.spectral(ARPES_dict)
#    
#    CD = (Igr-Igl)/(Igr+Igl)
#    print(abs(CD).max())
#        
#    w = np.linspace(*ARPES_dict['cube']['E'])
#    x = np.linspace(*ARPES_dict['cube']['X'])
#    W,X = np.meshgrid(w,x)
##    
#    fig = plt.figure()
#    ax= fig.add_subplot(111)
#    ax.pcolormesh(X,W,CD[0],cmap=cm.RdBu)
#    ax.set_ylim(-0.3,0.05)
