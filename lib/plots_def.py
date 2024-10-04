# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 16:30:22 2024

@author: gmart
"""
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator)
from matplotlib.ticker import MaxNLocator

def rrs_plot(xeje,yeje,output_dir,save_name)->float:
    fig                     =plt.figure(figsize=(15,10))
    ax                      =fig.add_axes([0.1,0.1,0.8,0.8])
    ax.plot(xeje,yeje,color="black",label="Rrs")
    ax.set_xlabel("Wavelength (nm)", fontsize=18)
    ax.set_ylabel("Rrs (Sr-1)", fontsize=18)
    ax.tick_params(axis='both', labelsize=20) 
    ax.grid(True)
    fig.savefig(output_dir+save_name+".jpg",dpi=300)
    plt.close(fig)

def ndci_plot(xeje,ndci_fil,sentinel_ndci,output_dir,save_name,filtro)->float:
    fig                     =plt.figure(figsize=(20,15))
    ax                      =fig.add_axes([0.1,0.1,0.8,0.8])
    ax.plot(xeje,ndci_fil,color="blue",label="ndci_fil")
    ax.plot(xeje,sentinel_ndci,color="black",label="ndci Sentinel",marker='o')
    if len(xeje)>=20:
        ax.xaxis.set_major_locator(MaxNLocator(nbins=20, integer=True))
    for tick in ax.get_xticklabels():
        tick.set_rotation(45)
    ax.set_ylabel("NDCI", fontsize=18)
    ax.tick_params(axis='both', labelsize=20) 
    ax.grid(True)
    plt.legend()
    fig.savefig(output_dir+save_name+".jpg",dpi=300)
    plt.close(fig)

def pcu_plot(xeje,yeje,std,output_dir,save_name,filtro)->float:
    fig                     =plt.figure(figsize=(20,15))
    ax                      =fig.add_axes([0.1,0.1,0.8,0.8])
    ax.plot(xeje,yeje,color="blue",label="PC$^μ$")
    ax.fill_between(xeje, yeje - std, yeje + std, color="#00BFFF", alpha=0.2, label="Std PC$^μ$")
    if filtro==True:
        ax.xaxis.set_major_locator(MultipleLocator(15))
    if filtro==False:
        ax.xaxis.set_major_locator(MultipleLocator(60))
    for tick in ax.get_xticklabels():
        tick.set_rotation(45)
    ax.set_ylabel("PC$^μ$", fontsize=18)
    ax.tick_params(axis='both', labelsize=20) 
    ax.grid(True)
    plt.legend()
    fig.savefig(output_dir+save_name+".jpg",dpi=300)
    plt.close(fig)
    
    
def chl_pcu(xeje,yeje,std,pcu,std_2,output_dir,save_name,filtro)->float:
    fig                     =plt.figure(figsize=(20,15))
    ax                      =fig.add_axes([0.1,0.1,0.8,0.8])
    ax.plot(xeje,yeje,color="green",label="Chlorophyll_wet")
    ax.plot(xeje,pcu,color="blue",label="PC$^μ$_wet")
    ax.fill_between(xeje, yeje - std, yeje + std, color="#013d02", alpha=0.2, label="Std Chlorophyll_wet")
    ax.fill_between(xeje, pcu  - std_2, pcu + std_2, color="#00BFFF", alpha=0.2, label="Std PC$^μ$_wet")
    if len(xeje)>=20:
        ax.xaxis.set_major_locator(MaxNLocator(nbins=20, integer=True))
    for tick in ax.get_xticklabels():
        tick.set_rotation(45)
    ax.set_ylabel("NDCI and PC$^μ$ index", fontsize=18)
    ax.tick_params(axis='both', labelsize=20) 
    ax.grid(True)
    plt.legend(loc='upper left',fontsize=18)
    fig.savefig(output_dir+save_name+".jpg",dpi=300)
    plt.close(fig)