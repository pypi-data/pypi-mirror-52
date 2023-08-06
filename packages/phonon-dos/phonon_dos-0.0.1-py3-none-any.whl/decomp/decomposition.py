#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 15:11:33 2019

@author: Gabriele Coiana
"""
import numpy as np
from decomp import cell, read, plot
import os

def corr(tall,X,tau,masses,mode):
    M = len(tall)
    dt = tall[1] - tall[0]
    tmax = M - tau
    N = np.size(X[0])   
    X0 = X[0:tmax,:]
    X2 = 1/tmax*np.sum(X[0:tmax,:]*X[0:tmax,:])
    C = []
    for n in range(tau):
        Xjj = X[n:n+tmax,:]
        a = np.multiply(np.conjugate(X0),Xjj)
        b = 1/(tmax) * np.sum(a,axis=0)#/X2
        c = np.multiply(b,1)
        if (mode=='projected'):
            d = c
        else:
            d = np.sum(c)
        C.append(d)
    C = np.array(C)
    t = np.arange(0,tau)*dt
    freq = np.fft.fftfreq(tau,d=dt)
    Z = np.fft.fft(C,axis=0)
    return t, C, freq, Z

# =============================================================================
# Parameters
a = read.read_parameters()[0]
mba, mti, mo = read.read_parameters()[1:4]
N1,N2,N3 = read.read_parameters()[4:7]
kinput = read.read_parameters()[7::][0]
file_eigenvectors = read.read_parameters()[8]
file_trajectory = read.read_parameters()[9]
file_initial_conf = read.read_parameters()[10]
system = read.read_parameters()[11]
DT = read.read_parameters()[12]
tau = read.read_parameters()[13]

N1N2N3 = N1*N2*N3 # Number of cells
N = N1*N2*N3*5    # Number of atoms
masses = np.repeat([mba, mti, mo, mo, mo],3)#*1822.9 #if you want atomic units, 1 a.u. = 1822.9 amu
# =============================================================================
print('\nHello, lets start!\n')
print(' Getting input parameters and calculating velocities...')
Nqpoints, qpoints_scaled, ks, freqs, eigvecs = read.read_phonopy(file_eigenvectors)

if (system=='norelax'):
    R0 = cell.BaTiO3(a).get_supercell(a,N1,N2,N3)  #cubic R0
if (system=='relax'):
    R0 = np.loadtxt('R0')                       #rhombo R0
    R0 = np.repeat(R0,3,axis=0)
if (system=='avg'):
    R0 = np.loadtxt('R0_avg')


Rt = np.loadtxt(file_trajectory)[:,1:]
Num_timesteps = int(len(Rt[:,0]))
print('\t Number of timesteps of simulation: ', Num_timesteps, '\n')
tall = np.arange(Num_timesteps)*DT*2.418884254*1e-05 #conversion to picoseconds
dt_ps = tall[1]-tall[0]
meta = int(Num_timesteps/2)
Vt = np.gradient(Rt,dt_ps,axis=0)  

print(' Done. Performing decomposition...\n')

flag = ''
anis = list(range(15))
for i in range(2):
    eigvec = eigvecs[i]
    freq_disp = freqs[i]
    k = ks[i]
    print('\t kpoint ',k)

    Vcoll = np.zeros((Num_timesteps,15),dtype=complex)  
    for j,h,l in zip(range(15),np.repeat(range(0,N),3)*N1N2N3*3,np.tile(range(0,3),5)):
        vels = np.array(Vt[:,h+l:h+N1N2N3*3:3],dtype=complex)
        poss = R0[h:h+N1N2N3*3:3,:]
        x = np.multiply(vels,np.exp(1j*np.dot(poss,k)))
        Vcoll[:,j] = 1/np.sqrt(N1N2N3)*np.sum(x,axis=1)
    Tkt = Vcoll*np.sqrt(masses)
    
    #eigvec_exp = np.array([0,0,0,0,0,0.5,0,0,-0.9,0,0,-0.6,0,0,0.6])
    #a = np.array([0,0,1,0,0,-1,0,0,-1,0,0,-1,0,0,-1])
    eigvecH = np.conjugate(eigvec.T)
    
    Qkt = np.dot(eigvecH,Tkt.T).T#.reshape(Num_timesteps,1)
    
    t, C, freq, Gtot = corr(tall,Tkt,tau, masses, ' ')
    Ztot = np.sqrt(np.conjugate(Gtot)*Gtot).real
    
    t, C, freq, G = corr(tall,Qkt,tau, masses, 'projected')
    Z = np.sqrt(np.conjugate(G)*G).real
    
    meta = int(len(t)/2)
    
    try:
        namedir = 'phonDOS_'+system
        os.mkdir(namedir)
        flag = 'created'
    except FileExistsError:
        if(flag=='created'):
            bbb = 1
        else:
            print('Folder '+namedir+' already exists. Rename it first! Interrupting code.')
            break
    for n in range(15):
        #plot.plot(freq[0:meta],Z[0:meta],'Spectrum of '+str(k))
        #anis[n] = plot.plot_with_ani(freq[0:meta],Z[0:meta,n],Ztot[0:meta], k, eigvec[:,n],freq_disp[n],n,file_eigenvectors,masses,10)
        plot.save_proj(freq[0:meta],Z[0:meta,n],Ztot[0:meta], k, eigvec[:,n],freq_disp[n],n,namedir)

    print('area of total ', np.trapz(Ztot*2.01578*1e-07,dx=freq[1]-freq[0]))
    kb = 3.1668085639379003*1e-06# a.u. [H/K]
    print('eqpt thm:', 1/2*kb*100)
#    print('area of sum of partials', np.sum(np.trapz(Z[:,3::],dx=freq[1]-freq[0],axis=0)))





