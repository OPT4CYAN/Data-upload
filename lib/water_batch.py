# -*- coding: utf-8 -*-
"""
Created on Wed May 31 14:21:16 2023

@author: doftdefault
"""
import os

def water_batch(doy, sentinel_dir)->float:
    import datetime
    from download_map  import download_map
    from bands_fun import bands_fun
    #first Download
    #declaracion de linelit para la memoria 
    download_dir                 = sentinel_dir+"downloads/"

    def dayofyear_to_date(dayofyear):
        year            = int(dayofyear / 1000)
        day             = int(dayofyear % 1000)
        date            = datetime.datetime(year, 1, 1) + datetime.timedelta(days=int(day)-1)
        return date.strftime("%Y-%m-%d")
    water = None
    date = dayofyear_to_date(doy)
    print("day: " + str(date) + " (" + str(doy) + ")")
    response = download_map(date, download_dir,'water')
    
    if response is not None:
        bands_fun(sentinel_dir)
        
        # remove
        for f in os.listdir(download_dir):
            os.remove(os.path.join(download_dir, f))
        print("Process completed for " + str(date))
    else:
        print("No satellite image for " + str(date))
        
    return water
        
