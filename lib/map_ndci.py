# -*- coding: utf-8 -*-
"""
Created on Fri May 26 11:39:04 2023

@author: doftdefault
"""
import numpy as np
import glob
from skimage import color
from PIL import Image
import matplotlib.pyplot as plt
import os
def map_ndci (ndci_array:float,destination_folder:str,name:str,origin_folder)->float:
   
    
    # Crear una máscara para los valores NaN en la matriz NDCI
    mask = np.isnan(ndci_array)
    
    # Aplicar la máscara para eliminar los valores NaN
    ndci_array_clean = np.ma.masked_array(ndci_array, mask)
    
    
    # Abrir la imagen TIFF
    dir_rgb= glob.glob(origin_folder + "/"+ "*rhos.tif")
    dir_rgb= dir_rgb[0]
    dir_rgb= dir_rgb.replace("\\","/")
    rgb_image = Image.open(dir_rgb)
    
    
    # Convertir la imagen RGB a escala de grises
    #puntos = [(SantaOlalla_lon, SantaOlalla_lat), (Lucio_lon, Lucio_lat), (Burro_lon, Burro_lat), (Duque_lon, Duque_lat)]
    gray_image = color.rgb2gray(rgb_image)
    
    os.chdir(destination_folder)
    fig                      = plt.figure(figsize=(15,10))
    plt.imshow(gray_image, cmap='gray',alpha=0.5)
    plt.imshow(ndci_array_clean, cmap='jet')
    plt.colorbar()
    plt.axis('off')
    #plt.scatter([p[0] for p in puntos], [p[1] for p in puntos], color='red', marker='x')
    fig.savefig(name[0:19] + "Ndci", dpi=300)
