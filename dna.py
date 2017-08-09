# Program using genetic algorithm to fit a kappa function
# DNA structure  - A,B or A,B,C in the functions
# created by Marcos Grala

import numpy as np
import random, math
import evolution as evo

# DNA when fitting with maxwellian distribution, only work with these two
class DNA_maxwellian:    
    def __init__(self):
        #remove append
        self.genes = [0]*2
        for i in xrange(2):
            self.genes[i] = random.random()
        
        self.fitness = -1
        self.correlation = -1
      
    def __str__(self):
        return str(self.correlation) + " " + str(1/self.genes[0]) + " " + str(self.genes[1])
    
    # calculate the fitness value for all elements
    def calcFitness(self,x,target,mean):
        coef = [1/self.genes[0],self.genes[1]]
        y_fit,mean_fit = evo.function(x,coef)
        dif = self.calcDiff(y_fit,target)
        self.fitness = 1/dif
    
    # calculate the difference between the function and the objective
    def calcDiff(self,y_fit,y_target):
        dif = 0
        size = len(y_fit)
        for i in xrange(size):
            #dif += (y_fit[i]-y_target[i])**2
            dif += ((y_fit[i]-y_target[i])/(y_target[i]))**2
        
        return np.sqrt(dif/(size-2))#/(y_target[0]-y_target[size-1])
        
    #correlation of the two functions
    def calcCorrelation(self,x,y_target,mean_target):
        
        coef = [1/self.genes[0],self.genes[1]]
        y,mean = evo.function(x,coef)
        size = len(x)
        
        yyfit = 0
        y2 = 0
        yfit2 = 0
        for i in xrange(size):
            yyfit += (y_target[i]-mean_target)*(y[i]-mean)
            y2    += (y_target[i]-mean_target)*(y_target[i]-mean_target)
            yfit2 += (y[i]-mean)*(y[i]-mean)
          
        s = np.sqrt(y2*yfit2)
        if s <1e-300: s = 1e-100
        cor = yyfit/s

        self.correlation = cor



## DNA when fitting with kappa distribution
class DNA_kappa:    
    def __init__(self):
        self.genes = [0]*3
        for i in xrange(3):
            num = random.random()
            if i==2: ## limit this value from 2.5 to 150
                while 1/num<=2.5 or 1/num>150: num = random.random()

            self.genes[i] = num

        self.fitness = -1
        self.correlation = -1
      
    def __str__(self):
        # output density, energy and kappa index
        A = 1/self.genes[0] 
        B = self.genes[1]
        C = 1/self.genes[2]

        kappa = C - 1
        KbT = 1/(B*(C-2.5))
        n = (5.946e-9)*A*B**(-1.5)*(math.gamma(C-1.5)/math.gamma(C))

        return str(self.correlation) + ", n = " + str(n) + ", KbT = " + str(KbT) + ", Kappa = " + str(kappa)
    # calculate the fitness value for all elements
    def calcFitness(self,x,target,mean):
        coef = [1/self.genes[0],self.genes[1],1/self.genes[2]]
        y_fit,mean_fit = evo.kappa(x,coef)
        dif = self.calcDiff(y_fit,target)
        self.fitness = 1/dif
    
    # calculate the difference between the function and the objective
    def calcDiff(self,y_fit,y_target):
        dif = 0
        size = len(y_fit)
        for i in xrange(size):
            dif += ((y_fit[i]-y_target[i])/(y_target[i]))**2
        
        return np.sqrt(dif/(size-2))
        
    #correlation of the two functions
    def calcCorrelation(self,x,y_target,mean_target):
        
        coef = [1/self.genes[0],self.genes[1],1/self.genes[2]]
        y,mean = evo.kappa(x,coef)
        size = len(x)
        
        yyfit = 0
        y2 = 0
        yfit2 = 0
        for i in xrange(size):
            yyfit += (y_target[i]-mean_target)*(y[i]-mean)
            y2    += (y_target[i]-mean_target)*(y_target[i]-mean_target)
            yfit2 += (y[i]-mean)*(y[i]-mean)
          
        s = np.sqrt(y2*yfit2)
        if s <1e-300: s = 1e-30
        cor = yyfit/s

        self.correlation = cor
        
