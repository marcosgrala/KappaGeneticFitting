#!/usr/bin/python2
# coding=utf-8
# author: Jose P. Marchezi
import datetime
import numpy as np
import glob
import os, re, ssl, urllib
from spacepy import pycdf
from scipy import interpolate as interp

# fill the gaps with nans
def fill_nan(A):
     '''
     interpolate to fill nan values
     '''
     if np.isnan(A[0]):
         A[0] = 0.5
     inds = np.arange(A.shape[0])
     good = np.where(np.isfinite(A))
     f = interp.interp1d(inds[good], A[good], bounds_error=False)
     B = np.where(np.isfinite(A), A, f(inds))
     return B

# Extract the variables of interest from mageis .cdf file
def extract_mageis(files_mageis, flag):
    var_mageis = ['Epoch', 'FEDU_Energy', 'FESA', 'FESA_ERROR']
    mageis = []
    for v in var_mageis:
        mageis.append([])
        for l in files_mageis:
            data_mageis = pycdf.CDF(l)
            mageis[len(mageis)-1].extend(data_mageis[v][...])

    for m in mageis[2]:
        m[m == -9999999999999999635896294965248.000] = 'NaN'
    for m in mageis[1]:
        m[m == -9999999848243207295109594873856.000] = 'NaN'
    if flag == 1:
        for l in files_mageis:
            os.remove(l)
    return mageis


def flux_values(year, month, day, hour, minute, second, download_data):
    ####
    # Data directory
    path = os.getcwd()
    dataDownlDir = path + '/data/'

    t_0 = datetime.datetime(int(year),01,01,0,0,0)
    instantEnergyDistr = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
    instSeconds = (instantEnergyDistr - t_0).total_seconds()
    str_temp_mageis = '.*(%04d%02d%02d).*' % (instantEnergyDistr.year, instantEnergyDistr.month, instantEnergyDistr.day)

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

    files_mageis = []
    for names in str_temp_mageis:
        local_file_mageis = dataDownlDir + '*' + names[3:-3] + '*'
        files_mageis.append(glob.glob(local_file_mageis)[0])
    files_mageis.sort()

    # read the mageis cdf file
    mageis = extract_mageis(files_mageis, 0)

    ## Separate the electron energy channels
    energy = np.asmatrix(mageis[2])[:,4:]
    error = np.asmatrix(mageis[3])[:,4:]
    energy_values = mageis[1][0][4:]
    # epoch
    magEpoch = mageis[0]

    for x in range(0,len(magEpoch)):
        if (magEpoch[x]-t_0).total_seconds() >= (instSeconds-10.9) and (magEpoch[x]-t_0).total_seconds() <= (instSeconds + 10.9):
            instant = x

    flux = []
    flux_error = []
    for x in range(0,len(energy_values)):
        flux.append(energy[instant,x])
        flux_error.append(error[instant,x])

    #nflux = fill_nan(np.asarray(flux))

    #return magEpoch, energy_values, nflux, flux_error
    return energy_values, flux
