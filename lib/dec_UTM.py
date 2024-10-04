# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 10:18:07 2023

@author: doftdefault
"""
import pyproj
#transformador de grados a UTM
def dec_UTM(lat:float,lon:float)->float:
    
    
    lat_decimal = lat
    lon_decimal = lon
    
    #  WGS 84 (latitud/longitud) y UTM
    wgs84 = pyproj.CRS("EPSG:4326")  
    utm = pyproj.CRS("EPSG:32629")   
    #conversión
    transformer = pyproj.Transformer.from_crs(wgs84, utm, always_xy=True)
    final_lon, final_lat = transformer.transform(lon_decimal, lat_decimal)
    
    return final_lon, final_lat
