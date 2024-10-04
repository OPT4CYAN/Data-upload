# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 14:47:58 2024

@author: gmart
"""
import numpy as np
def ponderar (data):
    for i in range(data.shape[0]):  # iteramos sobre filas
        for j in range(data.shape[1]):  # iteramos sobre columnas
            if np.isnan(data[i, j]):  # Si el valor es NaN
                # Buscar la fila no NaN más cercana por arriba
                fila_arriba = None
                for k in range(i-1, -1, -1):
                    if not np.isnan(data[k, j]):
                        fila_arriba = data[k, j]
                        break
                
                # Buscar la fila no NaN más cercana por abajo
                fila_abajo = None
                for k in range(i+1, data.shape[0]):
                    if not np.isnan(data[k, j]):
                        fila_abajo = data[k, j]
                        break
                
                # Si ambas filas no NaN existen, reemplazar NaN por la suma
                if fila_arriba is not None and fila_abajo is not None:
                    data[i, j] = fila_arriba + fila_abajo
    
    return data