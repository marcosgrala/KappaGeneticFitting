# Programm using genetic algorithm to fit a kappa function
# functions needed to evolve the populations
# created by Marcos Grala

import numpy as np
import random
import matplotlib.pyplot as plt
from dna import *

## evolve function
def evolve(functionType,populationSize,threshold,mutationRateBest,
           numberOfEvolution,x,y,mean):
    
    plt.loglog(x,y)
    plt.ion()

    population = [0]*populationSize
    if functionType == "kappa":
        for i in xrange(populationSize):
            solution = DNA_kappa()
            population[i] = solution
    elif functionType == "maxwellian":
        for i in xrange(populationSize):
            solution = DNA_maxwellian()
            population[i] = solution    
        
    population = sorting(population,x,y,mean)

    for t in xrange(numberOfEvolution):
        poolSelection = []
        poolSelection = selection(population,threshold)
        population = reproduction(poolSelection,population,threshold,
                                  populationSize,functionType)
        
        mutationRate = (t%100)/100.
        population = mutation(population,mutationRate,mutationRateBest)
        population = sorting(population,x,y,mean)
        if t%500==0 : 
            population[0].calcCorrelation(x,y,mean)
            print population[0]

            if functionType == "kappa":
                coef = [1/population[0].genes[0],population[0].genes[1],1/population[0].genes[2]]
                y_population,dumm = kappa(x,coef)
            elif functionType == "maxwellian":
                coef = [1/population[0].genes[0],population[0].genes[1]]
                y_population,dumm = function(x,coef)

            plt.loglog(x,y_population) 
            plt.pause(0.00005)

    plt.show(block=True)


        

####       functions needed        ###############################################
    
## add other functions here
def kappa(x,coef): ## KAPPA DISTRIBUTION FUNCTION
    size = len(x)
    func = np.zeros(size)
    mean = 0
    for i in xrange(size):
        func[i] = coef[0]*x[i]*(1+coef[1]*x[i])**(-coef[2])
        mean += func[i]
    mean = mean/size
    return func,mean
        
def function(x,coef): # FOR NOW MAXWELLIAN DISTRIBUTION
    size = len(x)
    func = np.zeros(size)
    mean = 0
    for i in xrange(size):
        func[i] = coef[0]*x[i]*np.exp(-coef[1]*x[i])
        mean += func[i]
    mean = mean/size
    return func,mean
    
def sorting(population,x,objective,mean):
    #calculate fitness function for all agents
    for solution in population:
        solution.calcFitness(x,objective,mean)
    
    # sort by fitness in decreasing order 
    newPopulation = sorted(population,key=lambda x: x.fitness, reverse=True)

    return newPopulation

    
def selection(population,limit):
    #create a new array with only limit%
    size = len(population)
    poolLimit = int(round(size*limit))
    totalFitnessOfBest = 0
    newAgents = population
    sizePoolRange = [0]*poolLimit
    
    for i in xrange(poolLimit):
        totalFitnessOfBest += newAgents[i].fitness

    sizePool = 0
    for i in xrange(poolLimit):
        newAgents[i].fitness = newAgents[i].fitness/totalFitnessOfBest
        sizePoolRange[i] = round(newAgents[i].fitness*size)
        sizePool += sizePoolRange[i]
    
    pool = [0]*int(sizePool)
    index = 0    

    for i in xrange(poolLimit):
        for t in xrange(int(sizePoolRange[i])):
            pool[index] = population[i]
            index += 1

    return pool
    
    
def reproduction(pool,population,limit,sizeTotal,functionType):
    #reproduce the rest of the population with new agents
    arrayLimit = int(len(population)*limit)
    newPopulation = [0]*sizeTotal
    for i in xrange(arrayLimit):
       newPopulation[i] = population[i]
    poolSize = len(pool)
    for r in xrange(arrayLimit,sizeTotal):
        parentA = pool[random.randrange(0,poolSize)]
        parentB = pool[random.randrange(0,poolSize)]
        #creates a child from parent A and B using a weight sum with random numbers
        if functionType=="kappa":
            child = DNA_kappa()
        elif functionType == "maxwellian":
            child = DNA_maxwellian()
        for i in xrange(len(child.genes)):
            fac = 0.5#random.random() #select the importance of the genes of each parent
            child.genes[i] = fac*parentA.genes[i]+(1-fac)*parentB.genes[i]

        newPopulation[r] = child

    return newPopulation   
        
    
def mutation(population,rate,rateBest):
    # mutate the population, with different chances for the best and the rest
    size = len(population)
    sizeGenes = len(population[0].genes)
    for i in xrange(size):
        if i==0:
            mutationRate = rateBest
        else:
            mutationRate = rate
        #chose one gene to mutate    
        index = random.randrange(0,sizeGenes)
        prob = random.random()
        if prob<mutationRate: population[i].genes[index] = random.random()

    return population

############################################################################################
  
