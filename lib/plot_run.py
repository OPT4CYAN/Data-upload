# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 11:53:03 2024

@author: gmart
"""

#haremos dos tipos de plots, sobre la rrs que puede ser interesante 
#y sobre pcu y ndci

import numpy as np
from datetime import datetime,timedelta
from plots_def import rrs_plot, ndci_plot, pcu_plot,chl_pcu

def plot_run (dir_input,today,site,sentinel_dir)->str:
    
    
    output_dir = dir_input +"plots/"+site+"/"
    rrs_all  =dir_input+site+"_rrs_all.dat" 
    index_all  =dir_input+site+"_index_all.dat" 
    ndci_dir   =dir_input +site+ "_ndci_filtered.dat"
    rrs_fil  =dir_input+site+"_rrs_filtered.dat"
    index_fil  =dir_input+site+"_index_filtered.dat"
    dirs_in         = [ndci_dir,index_all,rrs_fil,index_fil,rrs_all]
    dirs_name       =['ndci','index_all','rrs_fil','index_fil','rrs_all']
    dirs_data        = {}

###abrimos todos los archivos producidos tanto filtrados como no
    for i in range(len(dirs_in)):
        with open(dirs_in[i], "r") as doc:
            lines = doc.readlines()
    
        # Procesar las líneas y dividirlas por ';'
        linelist = [line.strip().split(";") for line in lines]
        # Convertir la lista de listas a un array de numpy
        dirs_data[dirs_name[i]]= np.array(linelist)
    linelist=np.array(linelist)
    ID_int                  = linelist[1:,0].astype(float).astype(int) 
    ID_str                  = ID_int.astype(str)
    wl                  = list(range(400,902,2))
    doy                 = [str(i[4:]) for i in ID_str]
    
    #cambiamos fechas a normal para aislar meses
    normal_fech              = ()
    for f in ID_str:
        temp=datetime.strptime(f[0:4] + f[4:], "%Y%j").strftime("%d-%m-%Y")
        normal_fech=np.append(normal_fech,temp)
    name_dic    = ['index_fil','index_all']
    for dic in name_dic:
        index_data = np.array(dirs_data[dic])[1:,:].astype(float)
        index_name          = dirs_data[dic][0,:]
        index_all           = {}
        
        for j in range(len(index_data[0,:])):
            temp=((abs(index_data[:,j])-np.nanmin(abs(index_data[:,j])))/(np.nanmax(abs(index_data[:,j]))-np.nanmin(abs(index_data[:,j]))))
            #temp=Smoo_filter(temp, 4) #suavizado
            index_all[index_name[j]]=temp  
            
        chl_name=['Chla_NDCI', 'Chla_G08', 'chla_OC4Me', 'CHL_m', 'CHL2D_m', 'CHL2C_m', 'CHL_P', 'CHL2_P']
        pcu_name=['PC_D', 'PC_SY', 'PC_S', 'PC_RV', 'PC_H3', 'PC_H1b',  'PC_L', 'PC_Br2' ]
        chl_temp = [index_all[var] for var in chl_name]
        chl_all = np.nanmean(chl_temp, axis=0)
        chl_std= np.nanstd(chl_temp,axis=0)
        dirs_data['ndci_'+dic] = index_all['NDCI']
        
        pcu_temp = [index_all[var] for var in pcu_name]
        pcu_all = np.nanmean(pcu_temp, axis=0)
        pcu_std = np.nanstd(pcu_temp,axis=0)
        dirs_data['pcu_'+dic]=pcu_all
        dirs_data['pcustd_'+dic]=pcu_std
        dirs_data['chl_'+dic]=chl_all
        dirs_data['chlstd_'+dic]=chl_std
    dirs_data['Santa_Olalla']=dirs_data['ndci'][1:,1].astype(float)
    dirs_data['Lucio_del_Rey']=dirs_data['ndci'][1:,2].astype(float)
    dirs_data['Hondon_del_Burro']=dirs_data['ndci'][1:,3].astype(float)
    dirs_data['Fuente_del_Duque']=dirs_data['ndci'][1:,4].astype(float)
    
    ##############################################################################    
    #all
    ##############################################################################
    rrs_all=dirs_data['rrs_fil'][1:,5:].astype(float)
    year_data=np.nanmean(rrs_all,axis=0)
    year_std= np.nanstd(rrs_all,axis=0)
    rrs_plot(wl,year_data,output_dir+"rrs/","alldays")
    

    chl_pcu(normal_fech,dirs_data['chl_index_fil'],dirs_data['chlstd_index_fil'],dirs_data['pcu_index_fil'],dirs_data['pcustd_index_fil'],output_dir+"chl/","alldays",False)
    
    ndci_plot(normal_fech,dirs_data['ndci_index_fil'],dirs_data[site],output_dir+"ndci/","alldays",False)
    
    ##############################################################################    
    #Rrs plot today
    ##############################################################################
    
    

    rrs_today               = dirs_data['rrs_fil'][1:,5:].astype(float)[np.where(ID_int==today)]
    todaymean               = np.nanmean(rrs_today,axis=0)
    date                    = int(today)
    chl_today               = chl_temp
    today                   =str(today)
    today_normal_fech=datetime.strptime(today[0:4] + today[4:], "%Y%j").strftime("%d-%m-%Y")
    rrs_plot(wl,todaymean,output_dir+"rrs/","today")
    rrs_plot(wl,todaymean,output_dir+"rrs/",today_normal_fech)
    
    ##############################################################################    
    #ndci plot -7 days
    ##############################################################################
    if len(ID_int)>7:
        normal_today = datetime.strptime(str(today)[0:4] + str(today)[4:], "%Y%j")
        normal_today_str = normal_today.strftime("%d-%m-%Y")
        day_7 = np.array([(normal_today - timedelta(days=i)).strftime("%d-%m-%Y") for i in range(7)])
        days_7 = [day for day in day_7 if day in normal_fech]
        if days_7:
            indice = [np.where(normal_fech == day)[0][0] for day in days_7]
            # Determinar el rango de días válidos
            days7 = normal_fech[min(indice):max(indice) + 1]
            pcu_7_fil=dirs_data['pcu_index_fil'][indice]
            pcu_7_all=dirs_data['pcu_index_all'][indice]
            ndci_7_fil=dirs_data['ndci_index_fil'][indice]
            ndci_7_all=dirs_data['ndci_index_all'][indice]
            chl_7_fil=dirs_data['chl_index_fil'][indice]
            chl_7_all=dirs_data['chl_index_all'][indice]
            sen_7=dirs_data[site][indice]
            
            pcustd_7_fil=dirs_data['pcustd_index_fil'][indice]
            chlstd_7_fil=dirs_data['chlstd_index_fil'][indice]
            
            chl_pcu(days7,chl_7_fil,chlstd_7_fil,pcu_7_fil,pcustd_7_fil,output_dir+"chl/","d-7",None)
            chl_pcu(days7,chl_7_fil,chlstd_7_fil,pcu_7_fil,pcustd_7_fil,output_dir+"chl/",str(normal_today_str)+"__7d",None)
            
            ndci_plot(days7,ndci_7_fil,sen_7,output_dir+"ndci/","d-7",None)
            ndci_plot(days7,ndci_7_fil,sen_7,output_dir+"ndci/",str(normal_today_str)+"__7d",None)
        
        
        else:
            days7 = np.array([]) 
        
    else:
        day_7=normal_fech
        days7=normal_fech
        
        pcu_7_fil=dirs_data['pcu_index_fil']
        pcu_7_all=dirs_data['pcu_index_all']
        ndci_7_fil=dirs_data['ndci_index_fil']
        ndci_7_all=dirs_data['ndci_index_all']
        chl_7_fil=dirs_data['chl_index_fil']
        chl_7_all=dirs_data['chl_index_all']
        sen_7=dirs_data[site]
       
        pcustd_7_fil=dirs_data['pcustd_index_fil']
        chlstd_7_fil=dirs_data['chlstd_index_fil']
    
        chl_pcu(days7,chl_7_fil,chlstd_7_fil,pcu_7_fil,pcustd_7_fil,output_dir+"chl/","d-7",None)
        chl_pcu(days7,chl_7_fil,chlstd_7_fil,pcu_7_fil,pcustd_7_fil,output_dir+"chl/",str(normal_today_str)+"__7d",None)
        
        ndci_plot(days7,ndci_7_fil,sen_7,output_dir+"ndci/","d-7",None)
        ndci_plot(days7,ndci_7_fil,sen_7,output_dir+"ndci/",str(normal_today_str)+"__7d",None)
    
    
    ##############################################################################    
    #ndci plot -30 days
    ##############################################################################
    if len(ID_int)>30:
        normal_today = datetime.strptime(str(today)[0:4] + str(today)[4:], "%Y%j")
        normal_today_str = normal_today.strftime("%d-%m-%Y")
        day_30 = np.array([(normal_today - timedelta(days=i)).strftime("%d-%m-%Y") for i in range(30)])
        days_30 = [day for day in day_30 if day in normal_fech]
        if days_30:
            indice = [np.where(normal_fech == day)[0][0] for day in days_30]
            # Determinar el rango de días válidos
            days30 = normal_fech[min(indice):max(indice) + 1]
            pcu_30_fil=dirs_data['pcu_index_fil'][indice]
            pcu_30_all=dirs_data['pcu_index_all'][indice]
            ndci_30_fil=dirs_data['ndci_index_fil'][indice]
            ndci_30_all=dirs_data['ndci_index_all'][indice]
            chl_30_fil=dirs_data['chl_index_fil'][indice]
            chl_30_all=dirs_data['chl_index_all'][indice]
            sen_30=dirs_data[site][indice]
            
            pcustd_30_fil=dirs_data['pcustd_index_fil'][indice]
            chlstd_30_fil=dirs_data['chlstd_index_fil'][indice]
            rrs_30=dirs_data['rrs_fil'][1:,5:].astype(float)[indice]
            chl_pcu(days30,chl_30_fil,chlstd_30_fil,pcu_30_fil,pcustd_30_fil,output_dir+"chl/","d-30",None)
            chl_pcu(days30,chl_30_fil,chlstd_30_fil,pcu_30_fil,pcustd_30_fil,output_dir+"chl/",str(normal_today_str)+"__30d",None)
            
            ndci_plot(days30,ndci_30_fil,sen_30,output_dir+"ndci/","d-30",None)
            ndci_plot(days30,ndci_30_fil,sen_30,output_dir+"ndci/",str(normal_today_str)+"__30d",None)
            
            rrs_plot(wl,todaymean,output_dir+"rrs/",str(normal_today_str)+"__30d")
            rrs_plot(wl,todaymean,output_dir+"rrs/",'d-30')
        
        else:
            days30 = np.array([]) 
        

    else:
        day_30=normal_fech
        days30=normal_fech
        
        pcu_30_fil=dirs_data['pcu_index_fil']
        pcu_30_all=dirs_data['pcu_index_all']
        ndci_30_fil=dirs_data['ndci_index_fil']
        ndci_30_all=dirs_data['ndci_index_all']
        chl_30_fil=dirs_data['chl_index_fil']
        chl_30_all=dirs_data['chl_index_all']
        sen_30=dirs_data[site]
        rrs_30=dirs_data['rrs_fil'][1:,5:].astype(float)
        pcustd_30_fil=dirs_data['pcustd_index_fil']
        chlstd_30_fil=dirs_data['chlstd_index_fil']
    
        chl_pcu(days30,chl_30_fil,chlstd_30_fil,pcu_30_fil,pcustd_30_fil,output_dir+"chl/","d-30",None)
        chl_pcu(days30,chl_30_fil,chlstd_30_fil,pcu_30_fil,pcustd_30_fil,output_dir+"chl/",str(normal_today_str)+"__30d",None)
        
        ndci_plot(days30,ndci_30_fil,sen_30,output_dir+"ndci/","d-30",None)
        ndci_plot(days30,ndci_30_fil,sen_30,output_dir+"ndci/",str(normal_today_str)+"__30d",None)
        
        todaymean               = np.nanmean(rrs_30,axis=0)
    
        rrs_plot(wl,todaymean,output_dir+"rrs/",str(normal_today_str)+"__30d")
        rrs_plot(wl,todaymean,output_dir+"rrs/",'d-30')
    
    ##############################################################################      
        #years
    
    ##############################################################################
    ##############################################################################      
        #Range select
        #filter 1 month
    
    ############################################################################## 
    #hayar meses
    rrs=dirs_data['rrs_fil'][1:,5:].astype(float)
    years                    = np.array([nf[6:] for nf in normal_fech])
    uniq_year                =np.unique(years)
    for y in uniq_year:
        indice_year             = np.where(y==years)[0]
        year_fech               =normal_fech[indice_year]
        
        year_pcu=dirs_data['pcu_index_all'][indice_year]
        year_pcu_dif=dirs_data['pcu_index_fil'][indice_year]
        year_chl=dirs_data['chl_index_all'][indice_year]
        year_chl_dif=dirs_data['chl_index_fil'][indice_year]
        year_ndci=dirs_data['ndci_index_all'][indice_year]
        year_ndci_dif=dirs_data['ndci_index_fil'][indice_year]
        year_pcu_std=dirs_data['pcustd_index_fil'][indice_year]
        year_chl_std=dirs_data['chlstd_index_fil'][indice_year]
        year_ndci_sen=dirs_data[site][indice_year] 
        year_rrs                = np.nanmean(dirs_data['rrs_fil'][1:,5:].astype(float)[indice_year],axis=0)
        
  
        rrs_plot(wl,year_rrs,output_dir+"rrs/",str(y))
        ndci_plot(year_fech,year_ndci_dif,year_ndci_sen,output_dir+"ndci/",str(y),False)
        ndci_plot(year_fech,year_ndci_dif,year_ndci_sen,output_dir+"ndci/","this_year",False)
        chl_pcu(year_fech,year_chl_dif,year_chl_std,year_pcu_dif,year_pcu_std,output_dir+"chl/",str(y),False)
        chl_pcu(year_fech,year_chl_dif,year_chl_std,year_pcu_dif,year_pcu_std,output_dir+"chl/","this_year",False)
        normal_year              = normal_fech[np.where(y==years)[0]]
        normal_month             = np.array([nf[3:5] for nf in normal_year])
        
        month                    ={}
        month_pcu                ={}
        month_pcu_std            ={}
        month_pcu_dif            ={}
        month_pcu_dif_std        ={}
        
        month_ndci               ={}
        month_ndci_dif           ={}
        month_ndci_sen           ={}
        
        month_chl                ={}
        month_chl_std            ={}
        month_chl_dif            ={}
        month_chl_dif_std        ={}
        days                     ={}
        month_name = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        month_numb = ['01','02','03','04','05','06','07','08','09','10','11','12']
        for m in range(len(month_name)):
            temp=np.where(normal_month==month_numb[m])[0]
            rrs_temp=rrs[temp]
            days[month_name[m]]=normal_year[np.where(normal_month==month_numb[m])[0]]
            month[month_name[m]]=np.nanmean(rrs_temp,axis=0)
            
            month_pcu[month_name[m]]=year_pcu[temp]
            month_pcu_dif[month_name[m]]=year_pcu_dif[temp]
            month_chl[month_name[m]]=year_chl[temp]
            month_chl_dif[month_name[m]]=year_chl_dif[temp]
            month_ndci[month_name[m]]=year_ndci[temp]
            month_ndci_dif[month_name[m]]=year_ndci_dif[temp]
            month_pcu_std[month_name[m]]=year_pcu_std[temp]
            month_chl_std[month_name[m]]=year_chl_std[temp]
            month_ndci_sen[month_name[m]]=year_ndci_sen[temp]
            
        for i in range(len(month)):
            if len(days[month_name[i]])!=0:
                rrs_plot(wl,month[month_name[i]],output_dir+"rrs/",month_name[i]+"_"+str(y))
                
                chl_pcu(days[month_name[i]],month_chl_dif[month_name[i]],month_chl_std[month_name[i]],month_pcu_dif[month_name[i]],month_pcu_std[month_name[i]],output_dir+"chl/",month_name[i]+"_"+str(y),True)
                ndci_plot(days[month_name[i]],month_ndci_dif[month_name[i]],month_ndci_sen[month_name[i]],output_dir+"ndci/",month_name[i]+"_"+str(y),True)
                chl_pcu(days[month_name[i]],month_chl_dif[month_name[i]],month_chl_std[month_name[i]],month_pcu_dif[month_name[i]],month_pcu_std[month_name[i]],output_dir+"chl/",month_name[i],True)
                ndci_plot(days[month_name[i]],month_ndci_dif[month_name[i]],month_ndci_sen[month_name[i]],output_dir+"ndci/",month_name[i],True)
    