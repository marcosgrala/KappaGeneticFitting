import numpy as np
import matplotlib.pyplot as plt
import energy as data
import math
import matplotlib
from matplotlib.offsetbox import AnchoredText


def kappa(x,n, kbt, kap): ## KAPPA DISTRIBUTION FUNCTION
    C = kap + 1
    B = 1 / (kbt * (C - 2.5))
    A = (n / ((5.946e-9)*(B**(-1.5)))) * (math.gamma(C) / math.gamma(C - 1.5))
    func = A*x[:]*(1+B*x[:])**(-C)
    mean = sum(func)/len(x)
    return func,mean

def maxw(x,n, kbt): # FOR NOW MAXWELLIAN DISTRIBUTION
    B = 1 / kbt
    A = n / ((B ** (-1.5)) * 5.946e-9)
    func = A * x[:] * np.exp(-B * x[:])
    mean = sum(func)/len(x)
    return func,mean

def plot_data(param_kappa, param_maxw,year, month, day, hour, minute, second, save_plot):

    xt,yt = data.flux_values(year, month, day, hour, minute, second)

    index = []
    #removing nan from arrays
    for i in xrange(len(xt)):
        if np.isnan(xt[i]) or np.isnan(yt[i]) or yt[i]<1.0:
            index.append(i)

            x = np.delete(xt,index)
            y = np.delete(yt,index)


    yy_k ,mean_k = kappa(x, param_kappa[0], param_kappa[1], param_kappa[2])

    yy_m, mean_m = maxw(x, param_maxw[0], param_maxw[1])

    matplotlib.rc('text', usetex=True)
    matplotlib.rc('font', family = 'arial', size = 12)
    matplotlib.rcParams['text.latex.preamble'] = [r'\usepackage{sfmath} \boldmath']


    title_twoFunc = '$%02d/%02d/%s$ - $%02d:%02d:%02d$  - $Kappa$ $e$ $Mawelliana$' %(int(day), int(month), str(year), int(hour), int(minute), int(second))
    title_kappa = '$%02d/%02d/%s$ - $%02d:%02d:%02d$  - $Kappa$' %(int(day), int(month), str(year), int(hour), int(minute), int(second))
    title_maxw = '$%02d/%02d/%s$ - $%02d:%02d:%02d$  - $Mawelliana$' %(int(day), int(month), str(year), int(hour), int(minute), int(second))
    figname_twoFunc = 'twoFunc_%s%02d%02d_%02d%02d%02d.png' %(str(year), int(month), int(day), int(hour), int(minute), int(second))
    figname_kappa = 'kappa_%s%02d%02d_%02d%02d%02d.png' %(str(year), int(month), int(day), int(hour), int(minute), int(second))
    figname_maxw = 'maxw_%s%02d%02d_%02d%02d%02d.png' %(str(year), int(month), int(day), int(hour), int(minute), int(second))

    # two functions
    plt.figure(figsize=(8, 7))
    plt.loglog(x,y, '.', label='$Dados$')
    plt.loglog(x,yy_k, label='$FD - \kappa$')
    plt.loglog(x,yy_m, label='$FD - m$')
    plt.legend()
    plt.grid()
    plt.ylabel('$Flux$ $[cm^{-2}s^{-1}keV^{-1}]$')
    plt.xlabel('$E$ $[keV]$')
    plt.title(title_twoFunc)
    plt.ylim([1, 5e5])


    if save_plot:
        plt.savefig(figname_twoFunc, format = 'png')

    # kappa
    plt.figure(figsize=(8, 7))
    plt.loglog(x,y, '.', label='$Dados$')
    plt.loglog(x,yy_k, label='$FD - \kappa$')
    plt.legend()
    plt.grid()
    plt.ylabel('$Flux$ $[cm^{-2}s^{-1}keV^{-1}]$')
    plt.xlabel('$E$ $[keV]$')
    plt.title(title_kappa)
    plt.ylim([1, 5e5])
    plt.text(30,20,"$\kappa = %.4f$\n$KbT = %.4f$\n$n = %.4f$" %(param_kappa[2], param_kappa[1], param_kappa[0]))


    if save_plot:
        plt.savefig(figname_kappa, format = 'png')

    # MAxwelliana
    plt.figure(figsize=(8, 7))
    plt.loglog(x,y, '.', label='$Dados$')
    plt.loglog(x,yy_m, label='$FD - m$')
    plt.legend()
    plt.grid()
    plt.ylabel('$Flux$ $[cm^{-2}s^{-1}keV^{-1}]$')
    plt.xlabel('$E$ $[keV]$')
    plt.title(title_maxw)
    plt.ylim([1, 5e5])
    plt.text(30,20,"$KbT = %.4f$\n$n = %.4f$" %(param_maxw[1], param_maxw[0]))


    if save_plot:
        plt.savefig(figname_maxw, format = 'png')


plot_data([0.0102483231877,  14.2045384407, 39.4750094769], [0.01116356564, 16.1137178057], 2014, 9, 12, 9, 30, 00, save_plot=True)
