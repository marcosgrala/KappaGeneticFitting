# Program using genetic algorithm to fit data with kappa or maxwellian distributions
# Created by Marcos Grala
import numpy as np
import evolution as evo
import energy as data
import os, datetime
import fnmatch


######    main program           #################################################333      
def main():
    populationSize = 200 # total size of popultion, maybe in the future reduce over time
    threshold = 0.10 # number of top population that will be used for reproduction
    mutationRateBest = 0.001 # chance to mutate de best solution
    numberOfEvolution = 100001 # max number o time steps
    functionType = "maxwellian" ## only works with kappa and maxwellian

    year = 2014
    month = 2
    day = 15

    #13 42 40
    #10 00 00
    xt,yt = data.flux_values(year, month, day, 10, 0, 0)

    index = []
    #removing nan from arrays
    for i in xrange(len(xt)):
        if np.isnan(xt[i]) or np.isnan(yt[i]) or yt[i]<1.0:
            index.append(i)

        x = np.delete(xt,index)
        y = np.delete(yt,index)

    #x = np.asarray(x)
    #y = np.asarray(y)
    #print x,y
    #
    #  creates data for test
    #  
    # kappa is defined here as 
    # y = A x ( 1 + B x )^-C
    # 
    # and maxwellian as
    # y = A x exp(-B x)
    #
    # Use three coeficients for kappa and two for maxwellian
    # if vector of y is given ignore this
    if len(y) == 0:
        coefs = [100,0.001,12] 
        if functionType=="kappa":
            y,mean = evo.kappa(x,coefs)
        elif functionType == "maxwellian":
            print "aqui"
            y,mean = evo.function(x,coefs)

    else:
    	mean = sum(y)/len(y)

    ####
    # main evolution of the code
    evo.evolve(functionType,populationSize,threshold,mutationRateBest,
          numberOfEvolution,x,y,mean)

    
if __name__ =="__main__":
    main()
