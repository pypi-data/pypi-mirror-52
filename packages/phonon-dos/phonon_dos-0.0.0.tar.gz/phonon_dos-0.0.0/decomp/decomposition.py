#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 15:11:33 2019

@author: Gabriele Coiana
"""
import numpy as np
import cell
import plot
import read
import yaml, os
yaml.warnings({'YAMLLoadWarning': False})

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
        b = 1/(tmax) * np.sum(a,axis=0)#/sigma2
        c = np.multiply(b,1)
        if (mode=='projected'):
            d = 1/N*(c)
        else:
            d = 1/N*np.sum(c)
        C.append(d)
    C = np.array(C)
    t = np.arange(0,tau)*dt
    freq = np.fft.fftfreq(tau,d=dt)
    Z = np.fft.fft(C,axis=0)
    return t, C, freq, Z

# =============================================================================
# 
ensemble = 'NVE'
system = 'norelax'


file_eigenvectors = 'qpoints_'+system+'_4.0.yaml'
datafile = 'data_pos_'+ensemble
N1,N2,N3 = 8,8,8
N1N2N3 = N1*N2*N3
N = N1N2N3*5
a = 8
masses = np.repeat([137.327, 47.867, 15.9994,15.9994,15.9994],3)#*1822.9 #if you want atomic units, 1 a.u. = 1822.9 amu
# =============================================================================

Nqpoints, qpoints_scaled, ks, freqs, eigvecs = read.read_phonopy(file_eigenvectors)

if (system=='norelax'):
    R0 = cell.BaTiO3(a).get_supercell(a,N1,N2,N3)  #cubic R0
if (system=='relax'):
    R0 = np.loadtxt('../R0')                       #rhombo R0
    R0 = np.repeat(R0,3,axis=0)
if (system=='avg'):
    R0 = np.loadtxt('../R0_avg')


Rt = np.loadtxt('../'+datafile)[:,1:]
Num_timesteps = int(len(Rt[:,0]))
print('Number of timesteps of simulation: ', Num_timesteps, '\n')
tall = np.arange(Num_timesteps)*30*30*2.418884254*1e-05 #conversion to picoseconds
dt = tall[1]-tall[0]
meta = int(Num_timesteps/2)
Vt = np.gradient(Rt,dt,axis=0)  
tau = 500

anis = list(range(15))
for i in range(1):
    eigvec = eigvecs[i]
    freq_disp = freqs[i]
    k = ks[i]

    Vcoll = np.zeros((Num_timesteps,15),dtype=complex)  
    for j,h,l in zip(range(15),np.repeat(range(0,N),3)*N1N2N3*3,np.tile(range(0,3),5)):
        vels = Vt[:,h+l:h+N1N2N3*3:3]
        poss = R0[h:h+N1N2N3*3:3,:]
        x = np.multiply(vels,np.exp(1j*np.dot(poss,k)))
        Vcoll[:,j] = 1/np.sqrt(N1N2N3)*np.sum(x,axis=1)
    Tkt = Vcoll*np.sqrt(masses)
    
#    eigvec_exp = np.array([0,0,0,0,0,0.5,0,0,-0.9,0,0,-0.6,0,0,0.6])
#    a = np.array([0,0,1,0,0,-1,0,0,-1,0,0,-1,0,0,-1])
    eigvecH = np.conjugate(eigvec.T)
    
    Qkt = np.dot(eigvecH,Tkt.T).T#.reshape(Num_timesteps,1)
    
    t, C, freq, Gtot = corr(tall,Tkt,tau, masses, ' ')
    Ztot = np.sqrt(np.conjugate(Gtot)*Gtot)
    
    t, C, freq, G = corr(tall,Qkt,tau, masses, 'projected')
    Z = np.sqrt(np.conjugate(G)*G)
    meta = int(len(t)/2)
    
    try:
        namedir = '../proj_'+ensemble+'_'+system
        os.mkdir(namedir)
    except FileExistsError:
        a=1
    for n in range(15):
        #plot.plot(freq[0:meta],Z[0:meta],'Spectrum of '+str(k))
        anis[n] = plot.plot_with_ani(freq[0:meta],Z[0:meta,n],Ztot[0:meta], k, eigvec[:,n],freq_disp[n],n,file_eigenvectors,masses,10)
        #plot.save_proj(freq[0:meta],Z[0:meta,n],Ztot[0:meta], k, eigvec[:,n],freq_disp[n],n,namedir)


    print('area of total ', np.trapz(Ztot,dx=freq[1]-freq[0]))
    print('area of sum of partials', np.sum(np.trapz(Z[:,3::],dx=freq[1]-freq[0],axis=0)))





