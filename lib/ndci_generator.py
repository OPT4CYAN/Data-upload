# -*- coding: utf-8 -*-
"""
Created on Wed May 17 11:36:29 2023

@author: doftdefault
"""
import netCDF4
import numpy as np
from map_ndci import map_ndci

def ndci_generator(dir_nc:str,destination_folder:str,name:str,origin_folder:str)->float:

    
    # environmental variables
    site_name           = ['Santa_Olalla','Lucio_del_Rey','Hondon_del_Burro','Fuente_del_Duque']
    site_latitude       = [         36.98,          36.92,             37.00,             37.00]
    site_longitude      = [         -6.48,          -6.35,             -6.42,             -6.43]
    site_heading        = [            45,              0,                 0,                45]
    
    
    # Abrir el archivo NetCDF en modo lectura
    dataset = netCDF4.Dataset(dir_nc, "r")
    
    # Obtener una lista de las variables disponibles en el archivo
    variables = dataset.variables
    lon= dataset.variables["lon"]
    lat= dataset.variables["lat"]
    ndci= dataset.variables["ndci"]
    
    # Acceder a los datos de la variable
    datos_lon = lon[:]
    datos_lat = lat[:]
    datos_ndci= ndci[:]
    dataset.close()
    
    #Crear imagen NDCI respecto a lat y lon
    # Convierte las matrices en arrays 
    lat_array = np.array(datos_lat)
    lon_array = np.array(datos_lon)
    ndci_array = np.array(datos_ndci)
    
    map_ndci (ndci_array,destination_folder,name,origin_folder)
    
    
    ##############################################################
    # el valor de ndci dependiendo de las estaciones 
    
    # coordenadas de las estaciones
    SantaOlalla_lat = site_latitude[0]
    SantaOlalla_lon = site_longitude[0]
    
    Lucio_lat = site_latitude[1]
    Lucio_lon = site_longitude[1]
    
    Burro_lat = site_latitude[2]
    Burro_lon = site_longitude[2]
    
    Duque_lat = site_latitude[3]
    Duque_lon = site_longitude[3]
    
    # Cálculo de las distancias
    dist_SantaOlalla = np.sqrt((lat_array - SantaOlalla_lat) ** 2 + (lon_array - SantaOlalla_lon) ** 2)
    dist_Lucio = np.sqrt((lat_array - Lucio_lat) ** 2 + (lon_array - Lucio_lon) ** 2)
    dist_Burro = np.sqrt((lat_array - Burro_lat) ** 2 + (lon_array - Burro_lon) ** 2)
    dist_Duque = np.sqrt((lat_array - Duque_lat) ** 2 + (lon_array - Duque_lon) ** 2)
    
    # Crea una máscara para identificar nan en ndci_array
    mask = np.isnan(ndci_array)
    
    # Aplicar la máscara 
    ndci_array_mask = ndci_array[~mask]
    lat_array_mask = lat_array[~mask]
    lon_array_mask = lon_array[~mask]
    
    #  nueva matriz  sin los valores NaN
    dist_SantaOlalla=dist_SantaOlalla[~mask]
    dist_Lucio = dist_Lucio[~mask]
    dist_Burro = dist_Burro[~mask]
    dist_Duque = dist_Duque[~mask]
    
    
    # Obtener valores de las 4 estaciones
    SantaOlalla_idx = np.unravel_index(np.nanargmin(dist_SantaOlalla), dist_SantaOlalla.shape)
    Lucio_idx = np.unravel_index(np.nanargmin(dist_Lucio), dist_Lucio.shape)
    Burro_idx = np.unravel_index(np.nanargmin(dist_Burro), dist_Burro.shape)
    Duque_idx = np.unravel_index(np.nanargmin(dist_Duque), dist_Duque.shape)
    
    # Valores NDCI
    SantaOlalla_ndci = ndci_array_mask[SantaOlalla_idx]
    Lucio_ndci = ndci_array_mask[Lucio_idx]
    Burro_ndci = ndci_array_mask[Burro_idx]
    Duque_ndci = ndci_array_mask[Duque_idx]
        
    #Hayar la nueva ubi para saber si esta muy lejana
    SantaOlalla_lat_dif = lat_array_mask[SantaOlalla_idx]
    SantaOlalla_lon_dif = lon_array_mask[SantaOlalla_idx]

    Lucio_lat_dif = lat_array_mask[Lucio_idx]
    Lucio_lon_dif = lon_array_mask[Lucio_idx]

    Burro_lat_dif = lat_array_mask[Burro_idx]
    Burro_lon_dif = lon_array_mask[Burro_idx]

    Duque_lat_dif = lat_array_mask[Duque_idx]
    Duque_lon_dif = lon_array_mask[Duque_idx]
    #diiferencia de distancia 
    
    #Se hace pitagoras para que el maximo aproximado sea 200m que h2=c2+c2 permite
    #despejar que son 14,1 pixels aprox, por lo que cada pixel son 10m aprox
    #total de 141m hacia cualquier dirección
    
    #SantaOlalla
    dif_lat= abs(SantaOlalla_lat- SantaOlalla_lat_dif)
    dif_lon= abs(SantaOlalla_lon - SantaOlalla_lon_dif)
    dif= dif_lat+dif_lon
    SantaOlalla=print("Santa_Olalla NDCI:", SantaOlalla_ndci)
    if dif> 0.0018:
        SantaOlalla_ndci= "Nan"
    #Lucio del Rey
    dif_lat= abs(Lucio_lat- Lucio_lat_dif)
    dif_lon= abs(Lucio_lon - Lucio_lon_dif)
    dif= dif_lat+dif_lon
    Lucio=print("Lucio_del_Rey NDCI:", Lucio_ndci)
    if dif> 0.0018:
        Lucio_ndci= "Nan"
    #Hondon del Burro
    dif_lat= abs(Burro_lat- Burro_lat_dif)
    dif_lon= abs(Burro_lon - Burro_lon_dif)
    dif= dif_lat+dif_lon
    Hondon=print("Hondon_del_Burro NDCI:", Burro_ndci)
    if dif> 0.0018:
        Burro_ndci= "Nan"
    #Duque
    dif_lat= abs(Duque_lat- Duque_lat_dif)
    dif_lon= abs(Duque_lon - Duque_lon_dif)
    dif= dif_lat+dif_lon
    Duque=print("Fuente_del_Duque NDCI:", Duque_ndci)
    if dif> 0.0018:
        Duque_ndci= "Nan"
        
    SantaOlalla=print("Santa_Olalla NDCI:", SantaOlalla_ndci)
    Lucio=print("Lucio_del_Rey NDCI:", Lucio_ndci)
    Hondon=print("Hondon_del_Burro NDCI:", Burro_ndci)
    Duque=print("Fuente_del_Duque NDCI:", Duque_ndci)
    
    return SantaOlalla_ndci, Lucio_ndci, Burro_ndci, Duque_ndci, ndci_array
    
   