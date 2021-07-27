#!/usr/bin/python
'''
Module: read_tropomi_no2_and_dump_ascii.py
==========================================================================================
Disclaimer: The code is for demonstration purposes only. Users are responsible to check for accuracy and revise to fit their objective.

Author: Justin Roberts-Pierel, 2015 
Organization: NASA ARSET
Purpose: To print all SDS from an TROPOMI file

Modified by Vikalp Mishra & Pawan Gupta, May 10 2019 to read TROPOMI data
==========================================================================================
'''
#!/usr/bin/python      
from netCDF4 import Dataset
import numpy as np
import sys
import time
import calendar
import datetime as dt
import pandas as pd


#This finds the user's current path so that all hdf4 files can be found
try:
    fileList=open('fileList.txt','r')
except:
    print('Did not find a text file containing file names (perhaps name does not match)')
    sys.exit()

#loops through all files listed in the text file
for FILE_NAME in fileList:
    FILE_NAME=FILE_NAME.strip()
    user_input=input('\nWould you like to process\n' + FILE_NAME + '\n\n(Y/N)')
    if(user_input == 'N' or user_input == 'n'):
        print('Skipping...')
        continue
    else:
        file = Dataset(FILE_NAME, 'r')
        grp='PRODUCT' 
# read the data
        if 'NO2' in FILE_NAME:
            print('This is a TROPOMI NO2 file.')
            #this is how you access the data tree in an hdf5 file
            SDS_NAME='nitrogendioxide_tropospheric_column'    
        elif 'AER_AI' in FILE_NAME:
            print('This is a TROPOMI Aerosol Index file.')
            SDS_NAME='aerosol_index_354_388'
        ds=file
        grp='PRODUCT'        
        lat= ds.groups[grp].variables['latitude'][0][:][:]
        lon= ds.groups[grp].variables['longitude'][0][:][:]
        data= ds.groups[grp].variables[SDS_NAME]      
        
        #get necessary attributes 
        fv=data._FillValue
          
        #get scan time and turn it into a vector
        scan_time= ds.groups[grp].variables['time_utc']
        # scan_time=geolocation['Time'][:].ravel()
        
        year = np.zeros(lat.shape)
        mth = np.zeros(lat.shape)
        doy = np.zeros(lat.shape)
        hr = np.zeros(lat.shape)
        mn = np.zeros(lat.shape)
        sec = np.zeros(lat.shape)
        
        for i in range(0,lat.shape[0]):
            t = scan_time[0][i].split('.')[0]
            t2 = dt.datetime.strptime(t,'%Y-%m-%dT%H:%M:%S')
            y = t2.year
            m = t2.month
            d = t2.day
            h = t2.hour
            m = t2.minute
            s = t2.second
            
            year[i][:] = y
            mth[i][:] = m
            doy[i][:] = d
            hr[i][:] = h
            mn[i][:] = m
            sec[i][:] = s
            
        vlist = list(file[grp].variables.keys())
        
        df = pd.DataFrame()
        df['Year'] = year.ravel()
        df['Month'] = mth.ravel()
        df['Day'] = doy.ravel()
        df['Hour'] = hr.ravel()
        df['Minute'] = mn.ravel()
        df['Second'] = sec.ravel()
        
        #This for loop saves all of the SDS in the dictionary at the top (dependent on file type) to the array (with titles)
        for i in range(0,len(vlist)):
            SDS_NAME=vlist[(i)] # The name of the sds to read
            #get current SDS data, or exit program if the SDS is not found in the file
            #try:
            sds=ds.groups[grp].variables[SDS_NAME]
            if len(sds.shape) == 3:
                print(SDS_NAME,sds.shape)
                #get attributes for current SDS
                if 'qa' in SDS_NAME:
                    scale=sds.scale_factor
                else: scale = 1.0
                fv=sds._FillValue

                #get SDS data as a vector
                data=sds[:].ravel()
                #The next few lines change fill value/missing value to NaN so that we can multiply valid values by the scale factor, then back to fill values for saving
                data=data.astype(float)
                data=(data)*scale
                data[np.isnan(data)]=fv
                data[data==float(fv)]=np.nan
                
                df[SDS_NAME] = data
    
    outfilename=FILE_NAME[:-3]+'.csv'    
    df.to_csv(outfilename, index = False)    
    print('\nAll files have been saved successfully.')