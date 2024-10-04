# -*- coding: utf-8 -*-
"""
Created on Thu May  4 15:42:06 2023

@author: doftdefault
"""
#Suavizado de index for plots
import numpy as np

def Smoo_filter (index:float,n:int)->float:
    index_                      = np.zeros((0,))
    # n this number is for the amount of surrounding data it takes to smooth
    for i in range(len(index)):
        if i < n:
            y                   = np.mean(index[i:i+(n+1)])
        elif i >= n and i != len(index) - n:
            y                   = np.mean(index[i-n:i+(n+1)])
        else:
            y                   = np.mean(index[i-n:len(index)])
        
        index_                  = np.append(index_, y)
    
    return index_