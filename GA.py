# Program using genetic algorithm to fit data with kappa or maxwellian distributions
# Created by Marcos Grala
import numpy as np
import evolution as evo

######    main program           #################################################333      
def main():
    populationSize = 200 # total size of popultion, maybe in the future reduce over time
    threshold = 0.10 # number of top population that will be used for reproduction
    mutationRateBest = 0.001 # chance to mutate de best solution
    numberOfEvolution = 100001 # max number o time steps
    functionType = "kappa" ## only works with kappa and maxwellian

    ####  DATA FOR TEST
    #

    x = [31.5,53.800,79.800,108.30,143.5,183.40,226.10,231.80,342.10,464.40,593.0,741.60,901.80,1077.7,1547.0,2275.0,2651.0,3681.0,4216.0]
    #y = [1.00330E5, 1.15040E5, 84808, 43422, 18279, 5773.5, 1291.6, 951.76, 18.142, 0.83207]#, 0.91806, 2.7590, 0.42957, 3.1449, 0.68470, 0.14919, 0.31496, 0.12885, 0.55581]
    y = []

    x = np.asarray(x)
    y = np.asarray(y)
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
