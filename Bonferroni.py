# Zhanchen Guo
# Bonferroni Simulation
# Python 2.7

# Uncomment the next line if using IPython for inline plotting
# %matplotlib inline
from __future__ import division
import numpy as np
import random
from scipy.stats import t

p = 0.1
CF = 0.95
population_size = 1000
population_type = 'normal'
alpha = 0.05
repeats = 10
trials = 1000
sample_size = 50
bonferroni = alpha / repeats

def t_test(x1, x2, s1, s2, n1, n2):
    return abs(x1 - x2) / ((s1 ** 2)/ (n1) + (s2 ** 2) / (n1)) ** 0.5

def create_pop(n, name=None):
    # A
    if name == None:
        distrib = 1000 * np.random.random_sample((n, ))
    elif name == 'binomial':
        distrib = np.random.binomial(n, p, (n, ))
    elif name == 'geometric':
        distrib = 1000 * np.random.geometric(p, (n, ))
    elif name == 'normal':
        distrib = np.random.normal(loc=100, scale=2, size=(n, ))
    elif name == 'exponential':
        distrib = np.random.exponential(size=(n,))
    return distrib

def sample_procedure(dist1, dist2):
    non_bon = 0
    bon = 0
    for i in xrange(trials):
        flag = True
        for _ in xrange(repeats):        
            # First sample
            sample1 = np.random.choice(dist1, (sample_size, ))
            mean1 = np.mean(sample1)
            std1 = np.std(sample1)

            # Second sample
            sample2 = np.random.choice(dist2, (sample_size, ))
            mean2 = np.mean(sample2)
            std2 = np.std(sample2)
                       
            # T test
            result = t_test(mean1, mean2, std1, std2, sample_size, sample_size)
            p_value = (1 - t.cdf(result, sample_size - 1)) * 2 
                                
            if p_value < alpha and flag:
                non_bon += 1
                flag = False
            if p_value < bonferroni:
                bon += 1
                break

    print "Time of reject in alpha: ", non_bon / trials
    print "Time of reject in bonferroni: ", bon / trials

#####################################
print "This is to prove Bonferroni Correction"
print "Hypothesis: The mean of the two population are same"
print "Firstly create two same(pseudo)-random distributions with both size of ", population_size
print "Population type is ", population_type

population1 = create_pop(population_size, population_type)
population2 = create_pop(population_size, population_type)

pop_mean1 = np.mean(population1)
pop_mean2 = np.mean(population2)
pop_std1 = np.std(population1)
pop_std2 = np.std(population2)
print "The population1 mean is:", pop_mean1
print "The population1 standard deviation is:", pop_std1
print "The population2 mean is:", pop_mean2
print "The population2 standard deviation is:", pop_std2
print "For the second step, drawing two sample at a time separately from both distribution",\
        "totally", repeats, "times",\
        "and then using comparision test to get t score, and then compare to alpha and",\
        "and corrected alpha sparately to whether the null hypothesis got rejected",\
        "At the end, repeat the process above for", trials, "times, and see how many",\
        "time null hypothesis got rejected. This is two tail test"


sample_procedure(population1, population2)

        