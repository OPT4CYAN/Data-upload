# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 11:40:04 2024

@author: gmart
"""

import pyproj
import netCDF4
from skimage import color
from PIL import Image
import subprocess
import codecs
import os
import glob
import numpy as np
import shutil
import rasterio
import pandas as pd
import datetime
import zipfile
import pathlib
import math
import json
import requests
import rasterio.warp
os.chdir('C:/Users/gmart/Proyectos/opt4cyan/lib')
import matplotlib.pyplot as plt
from read_TRSdata import read_TRSdata 
from sunposition import sunposition
from datetime import datetime,timedelta
from rasterio.transform import from_origin
from pre_run import pre_run
from index_run import index_run
from water_batch import water_batch
from NDCI_batch import NDCI_batch
from plot_run import plot_run
from renombr import renombr
from download_map  import download_map
from bands_fun import bands_fun
from mndwi_fun import mndwi_fun
from acolite_fun import acolite_fun
from plots_def import rrs_plot, ndci_plot, pcu_plot, chl_pcu
from Smoo_filter import Smoo_filter
from dec_UTM import dec_UTM
from ndci_generator import ndci_generator
from map_ndci import map_ndci
from index_alg import index_alg
from matplotlib.ticker import (MultipleLocator)
from ponderar import ponderar

input_dir          = "C:/Users/gmart/Proyectos/opt4cyan/input/"
output_dir         = "C:/Users/gmart/Proyectos/opt4cyan/output/"
temp_dir           = "C:/Users/gmart/Proyectos/opt4cyan/temp/"
sentinel_dir       = "C:/Users/gmart/Proyectos/opt4cyan/Sentinel/"
procesado          = "C:/Users/gmart/Proyectos/opt4cyan/datos_procesados/"
site               = ['Lucio_del_Rey','Hondon_del_Burro','Fuente_del_Duque','Santa_Olalla']
repro              = "C:/Users/gmart/Proyectos/opt4cyan/repro/"

def c_m_arch(Today,appended):
   with open(Today, 'a') as Today:
       Today.writelines(appended)
       print("Operación completada sin errores.")
#renombramos si es necesario
for i in site:
    repro_site=repro+i+"/"
    renombr(repro_site,i)
     
for i in site:
    repro_dir      =repro+i+"/"
    repro_data                         = glob.glob(repro_dir+ "*.dat") 
    for file in repro_data:
        shutil.move(file, input_dir)
        
        output_dir_site=output_dir+i+"/"
        pre_run(input_dir,output_dir_site,temp_dir,i)
        for f in os.listdir(input_dir):
            os.remove(os.path.join(input_dir, f)) 
        print("Arch ---->      Complete") 
#######index conversion
        ID=index_run(output_dir_site)
        print("Index Complete "+i+" Station")
        for f in os.listdir(input_dir):
            os.remove(os.path.join(input_dir, f)) 
        print("Arch ---->      Complete")   
        
doy=np.nanmax(ID.astype(int))    
#now, detect the water with sentinel-2       
water=water_batch(doy,sentinel_dir)
#procesing the Acolite program for detect the NDCI
NDCI_batch(doy,sentinel_dir)
print ("Ndci and water detection Complete "+str(doy))

###Date ndci water detection comparation ####
####usaremos ID de Santa_Olalla por que suele ser el que mas datos tiene####
for f in site:
    with open(sentinel_dir + "Today_mndwi.dat", "r") as sentinel_doc:
        lines = sentinel_doc.readlines()
    
    # Dividir las líneas por ';' y convertirlas a un array de numpy
    linelist = np.array([line.strip().split(";") for line in lines])
    
    # Extraer los títulos y los datos
    title_name = linelist[0, :]  # La primera fila son los títulos
    data = linelist[1:, 1:]  # Omitir la primera fila (títulos) y la primera columna (IDs)
    ID_sen = linelist[1:, 0].astype(int)  # Convertir la primera columna (ID_sen) a enteros
    
    # Reemplazar 'None' por np.nan y convertir los datos a float
    data = np.where(data == 'None', np.nan, data).astype(float)
    
    # Obtener los ID únicos
    ID_sen_uniq = np.unique(ID_sen)
    
    # Inicializar un array para almacenar los datos filtrados
    sen_data = np.zeros((0, data.shape[1]))
    
    # Calcular la media diaria para cada ID único
    for x in ID_sen_uniq:
        sen_temp = np.nanmean(data[ID_sen == x, :], axis=0)  # Media ignorando nan
        sen_data = np.vstack((sen_data, sen_temp))  # Añadir los datos filtrados

    with open(output_dir +f+ "/rrs_Today.dat", "r") as rrs_doc:
        lines = rrs_doc.readlines()
    # Procesar las líneas y dividirlas por ';'
    linelist_rrs = [line.strip().split(";") for line in lines]
    # Convertir la lista de listas a un array de numpy
    linelist_rrs = np.array(linelist_rrs)
    data_rrs    =   linelist_rrs[1:,:].astype(float)
    ID          = linelist_rrs[1:,0].astype(int)
    # Ahora procesamos los IDs y clonamos los datos
    ID_uniq = np.unique(ID)
    sentinel_clone = np.full((len(ID_uniq), sen_data.shape[1]), np.nan)
    
    # Rellenar sentinel_clone con los datos correspondientes a cada ID
    for unq in ID_sen_uniq:
        indice = np.where(ID_uniq == unq)[0]
        sentinel_clone[indice, :] = sen_data[ID_sen_uniq == unq, :]
    
    # Apilar los IDs únicos y los datos procesados
    sentinel_doc = np.column_stack((ID_uniq, sentinel_clone))
    
    # Añadir los títulos en la primera fila
    sentinel_doc = np.vstack((title_name, sentinel_doc))
    
    # Guardar los resultados en un archivo
    np.savetxt(procesado + str(f)+'_mndwi_filtered.dat', sentinel_doc, delimiter=';', fmt='%s')
    # Save de sentinel clone
    # Cargar el archivo Today_ndci.dat
    # Cargar el archivo Today_ndci.dat
    # Cargar el archivo Today_ndci.dat
    with open(sentinel_dir + "Today_ndci.dat", "r") as ndci_doc:
        lines = ndci_doc.readlines()
    
    # Dividir las líneas por ';' y convertirlas a un array de numpy
    linelist = np.array([line.strip().split(";") for line in lines])
    
    # Extraer los títulos y los datos
    title_name = linelist[0, :]  # La primera fila son los títulos
    data = linelist[1:, 1:]  # Omitir la primera fila (títulos) y la primera columna (IDs)
    ID_sen = linelist[1:, 0].astype(int)  # Convertir la primera columna (ID_sen) a enteros
    
    # Reemplazar 'None' por np.nan y convertir los datos a float
    data = np.where(data == 'None', np.nan, data).astype(float)
    
    # Obtener los ID únicos
    ID_sen_uniq = np.unique(ID_sen)
    
    # Inicializar un array para almacenar los datos filtrados
    sen_data = np.zeros((0, data.shape[1]))
    
    # Calcular la media diaria para cada ID único
    for x in ID_sen_uniq:
        sen_temp = np.nanmean(data[ID_sen == x, :], axis=0)  # Media ignorando nan
        sen_data = np.vstack((sen_data, sen_temp))  # Añadir los datos filtrados
    
    # Ahora procesamos los IDs y clonamos los datos
    ID_uniq = np.unique(ID)
    ndci_clone = np.full((len(ID_uniq), sen_data.shape[1]), np.nan)
    
    # Rellenar ndci_clone con los datos correspondientes a cada ID
    for unq in ID_sen_uniq:
        indice = np.where(ID_uniq == unq)[0]
        ndci_clone[indice, :] = sen_data[ID_sen_uniq == unq, :]
    
    # Apilar los IDs únicos y los datos procesados
    ndci_doc = np.column_stack((ID_uniq, ndci_clone))
    
    # Añadir los títulos en la primera fila
    ndci_doc = np.vstack((title_name, ndci_doc))
    
    # Guardar los resultados en un archivo
    np.savetxt(procesado + str(f)+'_ndci_filtered.dat', ndci_doc, delimiter=';', fmt='%s')



    sentinel_clone=sentinel_clone.astype(float)
    sentinel_clone[sentinel_clone>=0]=1
    sentinel_clone[sentinel_clone<0]=0
    #ponderamos los nan a la presencia o no de 1 en el entorno 
    binary_code= ponderar(sentinel_clone)
    binary_code[binary_code>0]=1
    binary_code[binary_code!=0]=1  
    

#abrimos los archivos para filtrar con los dias del agua 
    with open(output_dir +f+ "/rrs_Today.dat", "r") as rrs_doc:
        lines = rrs_doc.readlines()
    # Procesar las líneas y dividirlas por ';'
    linelist_rrs = [line.strip().split(";") for line in lines]
    # Convertir la lista de listas a un array de numpy
    linelist_rrs = np.array(linelist_rrs)
    data_rrs    =   linelist_rrs[1:,:].astype(float)
    #media diaria, ya que hay varias medidas para los dias
    data_mean_rrs = np.zeros((0, data_rrs.shape[1]))
    for x in np.unique(data_rrs[:,0].astype(int)):
        temp=np.where(data_rrs[:,0].astype(int)==x)[0]
        data_temp = np.nanmean(data_rrs[temp,:], axis=0)  # Media ignorando nan
        data_mean_rrs = np.append(data_mean_rrs,[data_temp],axis=0)
    data_all_rrs=np.vstack((linelist_rrs[0,:], data_mean_rrs))
    np.savetxt(procesado +str(f)+'_rrs_all.dat', data_all_rrs, delimiter=';', fmt='%s')
    with open(output_dir +f+ "/index_Today.dat", "r") as index_doc:
        lines = index_doc.readlines()
    # Procesar las líneas y dividirlas por ';'
    linelist_index = [line.strip().split(";") for line in lines]
    # Convertir la lista de listas a un array de numpy
    linelist_index = np.array(linelist_index)
    data_index    =   linelist_index[1:,:].astype(float)
    #media diaria, ya que hay varias medidas para los dias
    data_mean_index = np.zeros((0, data_index.shape[1]))
    for x in np.unique(data_index[:,0].astype(int)):
        temp=np.where(data_index[:,0].astype(int)==x)[0]
        data_temp = np.nanmean(data_index[temp,:], axis=0)  # Media ignorando nan
        data_mean_index = np.append(data_mean_index,[data_temp],axis=0)
        data_all_index=np.vstack((linelist_index[0,:], data_mean_index))
        np.savetxt(procesado +str(f)+'_index_all.dat', data_all_index, delimiter=';', fmt='%s')
    if f=='Santa_Olalla':
        code=binary_code[:,0]
    if f=='Lucio_del_Rey':
        code=binary_code[:,1]
    if f=='Hondon_del_Burro':
        code=binary_code[:,2]
    if f=='Fuente_del_Duque':
        code=binary_code[:,3]
#filtrar con binry code para dias de agua
    for cd in range(len(code)):
        temp=data_mean_rrs[cd,5:]*code[cd]
        data_mean_rrs[cd,5:]=temp
        temp=data_mean_index[cd,3:]*code[cd]
        data_mean_index[cd,3:]=temp
    data_mean_rrs[data_mean_rrs==0]=np.nan
    data_mean_rrs=np.vstack((linelist_rrs[0,:], data_mean_rrs))
    data_mean_index[data_mean_index==0]=np.nan
    data_mean_index=np.vstack((linelist_index[0,:], data_mean_index))
    
    np.savetxt(procesado +str(f)+'_rrs_filtered.dat', data_mean_rrs, delimiter=';', fmt='%s')
    np.savetxt(procesado +str(f)+'_index_filtered.dat', data_mean_index, delimiter=';', fmt='%s')
    
    #datso procesados de forma completa, comienzo a plotear
    print("Process completed ----> Plots start")
        
    plot_run(procesado,doy,f,sentinel_dir)
    






   