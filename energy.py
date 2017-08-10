#!/usr/bin/python2
# coding=utf-8
# author: Jose P. Marchezi
import datetime
import numpy as np
import glob
import os, re, ssl, urllib,fnmatch
from spacepy import pycdf
from scipy import interpolate as interp

# Extract the variables of interest from mageis .cdf file
def extract_mageis(files_mageis, flag, dir):
    var_mageis = ['Epoch', 'FEDU_Energy', 'FESA', 'FESA_ERROR']
    mageis = []
    for v in var_mageis:
        mageis.append([])
        
        data_mageis = pycdf.CDF(dir+files_mageis)
        mageis[len(mageis)-1].extend(data_mageis[v][...])

    for m in mageis[2]:
        m[m == -9999999999999999635896294965248.000] = 'NaN'
    for m in mageis[1]:
        m[m == -9999999848243207295109594873856.000] = 'NaN'
    if flag == 1:
        for l in files_mageis:
            os.remove(l)
    return mageis


def flux_values(year, month, day, hour, minute, second):
    ####
    # Data directory
    path = os.getcwd()
    
    if not os.path.exists(path + '/data/'):
        os.makedirs(path + '/data/')
        
    dataDownlDir = path + '/data/'
     
    instantEnergyDistr = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
   
    str_temp_mageis = '.*(%04d%02d%02d).*' % (instantEnergyDistr.year, instantEnergyDistr.month, instantEnergyDistr.day)
    date = '%04d%02d%02d' % (instantEnergyDistr.year, instantEnergyDistr.month, instantEnergyDistr.day)
    

    ##see if file already exists
    download_data = True
    for file in os.listdir(dataDownlDir):
        if fnmatch.fnmatch(file, '*'+date+'*'):
            download_data = False
            files_mageis = file
   

    if download_data:
        print('Downloading the VAP-A-MagEis data... \n\n')
        # define the directory and host in the https
        host = 'https://rbsp-ect.lanl.gov/data_pub/rbspa/mageis/level2/sectors/%s/' % (str_temp_mageis[3:7])
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        ssl._create_default_https_context = ssl._create_unverified_context
        # open the url
        a = urllib.urlopen(host, context=ctx)
        # read all the content of the page
        bb = a.readlines()
        aa = []
        regex = re.compile(str_temp_mageis)
        # extract the desired filename
        aa = [m.group(0) for l in bb for m in [regex.search(l)] if m][0].split('"')[7]
        # download the file
        downfile = urllib.URLopener()
        downfile.retrieve(host+aa, dataDownlDir+aa)
        print('Downloaded: ' + aa)
        files_mageis = aa

    # read the mageis cdf file
    mageis = extract_mageis(files_mageis, 0,dataDownlDir)

    ## Separate the electron energy channels
    energy = np.asmatrix(mageis[2])[:,4:]
    error = np.asmatrix(mageis[3])[:,4:]
    energy_values = mageis[1][0][4:]
    # epoch
    magEpoch = mageis[0]

    
    minDif = 0
    for x in range(0,len(magEpoch)):
        #print (magEpoch[x+1]-magEpoch[x]).total_seconds()
        localDif = abs((magEpoch[x]-instantEnergyDistr).total_seconds())
        #if (magEpoch[x]-t_0).total_seconds() >= (instSeconds-10.9) and (magEpoch[x]-t_0).total_seconds() <= (instSeconds + 10.9):
        if localDif<minDif or x==0:
            instant = x
            minDif = localDif
           
    print minDif, instant
    flux = []
    flux_error = []
    for x in range(0,len(energy_values)):
        flux.append(energy[instant,x])
        flux_error.append(error[instant,x])

    #nflux = fill_nan(np.asarray(flux))

    #return magEpoch, energy_values, nflux, flux_error
    return energy_values, flux
