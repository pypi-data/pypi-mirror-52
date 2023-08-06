#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 13 14:12:07 2019

@author: gc4217
"""
import numpy as np
import os

def avg_vs_t(time,quantity):
    avg = []
    for i in range(1,len(time)):
        dt = time[i]-time[i-1]
        y = quantity[0:i]
        integral = np.sum(dt*y,axis=0)
        avg.append(1/(i*dt)*integral)
    avg = np.array(avg)
    return avg


N1, N2, N3 = sys.argv[1], sys.argv[2], sys.argv[3]
N1N2N3 = N1*N2*N3
N = N1*N2*N3*5

with open('Cartesian_0','r') as f:
    A = f.readlines()
a = 0
for i in range(0,len(A),N+1):
    del A[i-a]
    a = a + 1
    
with open('pos','w') as g:
    g.writelines(A)
    
Rall = np.loadtxt('pos',usecols=(1,2,3))

Num_timesteps = int(len(Rall)/N)
t = np.arange(Num_timesteps-1)*30*30*2.418884254*1e-05 #conversion to picoseconds

R = []
for i in range(0,len(Rall),N):
    if(i==N):
        continue
    #pos_first_Ba = Rall[i:i+1,:]
    #pos_cm = np.sum(Rall[i:i+N,:],axis=0)/N
    
    to_write = Rall[i:i+N:1] #- pos_cm
    R.append(to_write.flatten())
    
R = np.array(R)

data_pos = np.hstack((t.reshape(len(t),1),R))

runn_avg = avg_vs_t(t,R)
data_avg = np.hstack((t[1::].reshape(len(t[1::]),1),runn_avg))

np.savetxt('runn_avg_pos',data_avg)
np.savetxt('data_pos',data_pos)


os.remove('pos')


























