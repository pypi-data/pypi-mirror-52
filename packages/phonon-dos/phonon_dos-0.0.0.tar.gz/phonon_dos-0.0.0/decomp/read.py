#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 16:14:34 2019

@author: gabriele
"""
import numpy as np
import yaml
#yaml.warnings({'YAMLLoadWarning': False})

def read_phonopy(file_eigenvectors):
    ## =============================================================================
    # Phonopy frequencies and eigenvectors
    data = yaml.load(open('../'+file_eigenvectors))
    #D = data['phonon'][0]['dynamical_matrix']
    #D = np.array(D)
    #D_real, D_imag = D[:,0::2], 1j*D[:,1::2]
    #D = (D_real + D_imag)*21.49068**2#*0.964*10**(4)#
    
    data2 = data['phonon']
    qpoints_scaled = []
    freqs = []
    eigvecs = []
    for element in data2:
        qpoints_scaled.append(element['q-position'])
        freq = []
        eigvec = np.zeros((15,15),dtype=complex)
        for j in range(len(element['band'])):
            branch = element['band'][j]
            freq.append(branch['frequency'])
            
            eigen = np.array(branch['eigenvector'])
            eigen_real = eigen[:,:,0]
            eigen_imag = eigen[:,:,1]
            eigen = eigen_real + 1j*eigen_imag
            eigen = eigen.reshape(15,)
            eigvec[:,j] = eigen
    
        freqs.append(freq)
        eigvecs.append(eigvec)
    qpoints_scaled = np.array(qpoints_scaled)
    freqs = np.array(freqs)
    Nqpoints = len(qpoints_scaled[:,0])
    
    
    c = 1.88973 #conversion to Bohrs
    Hk = np.array(data['reciprocal_lattice'])*2*np.pi*1/c
    ks = np.dot(Hk,qpoints_scaled.T).T
    # =============================================================================
    return Nqpoints, qpoints_scaled, ks, freqs, eigvecs