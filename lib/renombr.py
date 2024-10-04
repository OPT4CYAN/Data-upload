# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 13:25:40 2024

@author: gmart
"""
import numpy as np
import glob
import os

def renombr(repro_site,site)->str:
    input_data                         = glob.glob(repro_site+ "data*")
    if len(input_data)!=0:
        file_names = np.array([os.path.basename(file) for file in input_data])
        code=0
        for put in range(len(file_names)):
            numb=int(file_names[put][(file_names[put].find("data")+len("data")):(file_names[put].find(".dat"))])
            if len(str(numb))>3:
                numb=int(file_names[put][(file_names[put].find("data")+len("data")):(file_names[put].find("_2"))])
            if len(str(numb))<3:
                form_numb='{:05}'.format(numb)
            else:
                form_numb=numb
            fecha='_'+str(200000000000+code)
            code=code+1
            if site=='Santa_Olalla':
                name='solalla_data'
            if site=='Lucio_del_Rey':
                name='luciorey_data'
            if site=='Hondon_del_Burro':
                name='hburro_data'
            if site=='Fuente_del_Duque':
                name='fuenteduque_data'
                    
            rename=name+str(form_numb)+fecha+'.dat'
            os.rename(input_data[put],repro_site+rename)
    
    input_data                         = glob.glob(repro_site+ "*.dat")
    file_names = np.array([os.path.basename(file) for file in input_data])
    for put in range(len(file_names)):
        numb=int(file_names[put][(file_names[put].find("_data")+len("_data")):(file_names[put].find("_2"))])
        if len(str(numb))<5:
            form_numb='{:05}'.format(numb)
            rename=file_names[put][:(file_names[put].find("data")+len("data"))]+form_numb+file_names[put][(file_names[put].find("_2")):]
            os.rename(input_data[put],repro_site+rename)
                
                
                
                
