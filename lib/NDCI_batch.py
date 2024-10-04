# -*- coding: utf-8 -*-
"""
Created on Wed May 31 14:21:16 2023

@author: doftdefault
"""
import datetime 
from download_map  import download_map
from acolite_fun import acolite_fun
import os
#hay que hacerlo funcion otra vez, es todo un tabulado menos def
def NDCI_batch(doy,root_dir)->float:
    
    download_dir                 = root_dir+"downloads/"

    def dayofyear_to_date(dayofyear):
        year            = int(dayofyear / 1000)
        day             = int(dayofyear % 1000)
        date            = datetime.datetime(year, 1, 1) + datetime.timedelta(days=int(day)-1)
        return date.strftime("%Y-%m-%d")
    
    date = dayofyear_to_date(doy)
    response = download_map(date,download_dir,'ndci')
    if response == "ok":
        # Decompress and acolite
        print("Download ok  " + str(date))
        acolite_fun(root_dir)
        # Clear tmp files
        for f in os.listdir(download_dir):
            os.remove(os.path.join(download_dir, f))
        print("Process completed for  " + str(date))
    else:
        print("No satellite image for  " + str(date))