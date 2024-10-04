# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 02:15:37 2024

@author: gmart
"""
import numpy as np
from index_alg import index_alg

def index_run (output_dir)->str:

    #abrimos el archivo hecho por el grupo 1
    with open(output_dir + "rrs_Today.dat", "r") as rrs_doc:
        lines = rrs_doc.readlines()
 
    # Procesar las líneas y dividirlas por ';'
    linelist = [line.strip().split(";") for line in lines]
 
    # Convertir la lista de listas a un array de numpy
    linelist = np.array(linelist)
   
    #necesitamos seleccionar solo la rrs de las columnas y la fecha doy y year
    ID                  = linelist[1:,0].astype(int)
    doy                 = linelist[1:,2].astype(float)
    year                = linelist[1:,1].astype(int)
    Rrs                 = linelist[1:,5:].astype(float)
    #comenzamos con los indices, para ello habremos seleccionado algunos
    index_data,index_name          = index_alg(Rrs)  
    
    
    #creamos el codigo otra vez para guardarlo en .dat 
    def c_m_arch(Today,appended):
        # Copy current file to previous file (rename)
        # Open the current file in append mode (append to the end)
        with open(Today, 'a') as Today:
            Today.writelines(appended)
    
    Today                               = output_dir+ "index_Today" +".dat"
    title                               =["ID","Year","Doy"] 
    
    with open(Today, 'w') as archivo:
       # Convertir columna3 en una cadena de texto donde cada valor está separado por un ;
       columna2_str = ';'.join(map(str, index_name))
       columna1_str = ';'.join(map(str, title))
    
     # Escribir los datos en una fila, con los valores de columna3 como columnas separadas por ;
       archivo.write(columna1_str + ";"+columna2_str+"\n")
        #crea yesterday
    index_data             = np.transpose(index_data)
    for data in range(len(index_data)):
        columna2_str = ';'.join(map(str, index_data[data,:]))
        appended     =  (str(ID[data])+";"+str(int(year[data]))+";"+str(doy[data])+";"+columna2_str+"\n")
        c_m_arch(Today,appended)
    print("Appended Today and Yesterday")
    return ID