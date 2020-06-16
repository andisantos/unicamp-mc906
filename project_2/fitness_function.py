import numpy as np
import defines as df
from operator import itemgetter
import sys
import os

def fitness(individual, wishlist, gifts):
    score = 0

    for child, gift in enumerate(individual):
        # Check if the gift is on child whishlist.
        # Computes its score based on position. 
        try:
            wishlist_score = df.n_wishlist - np.where(wishlist[child] == gift)[0][0]
        except:
            wishlist_score = -df.n_wishlist

        # Compute gift happines score score based on position.
        gifts_score = df.n_gift_types - np.where(gifts[child] == gift)[0][0]

        total_score = (wishlist_score/df.n_wishlist) + (gifts_score/df.n_gift_types)
        score += total_score/2

    # total score is the mean of child and gift happiness
    return score/df.n_children

def rank_fitness(generation):
    gifts = np.loadtxt("dataset/gifts_"+str(df.n_children)+".csv", dtype=np.int32, delimiter=",")
    wishlist = np.loadtxt("dataset/wishlist_"+str(df.n_children)+".csv", dtype=np.int32, delimiter=",")

    fitlist = np.asarray([fitness(individual, wishlist, gifts) for individual in generation])
    np.set_printoptions(threshold=sys.maxsize)
    generation = np.asarray([x for _, x in sorted(zip(fitlist, generation), key=itemgetter(0), reverse=True)])

    if not os.path.exists('outputs/'+df.configs):
        os.makedirs('outputs/'+df.configs)
    with open('outputs/'+df.configs+'/averages.txt','a') as f:
        f.write(str(np.average(fitlist))+'\n')
    with open('outputs/'+df.configs+'/maxs.txt','a') as f:
        f.write(str(np.max(fitlist))+'\n')
    with open('outputs/'+df.configs+'/mins.txt','a') as f:
        f.write(str(np.min(fitlist))+'\n')

    return generation

def roulette_fitness(generation): #no pain no gain
    gifts = np.loadtxt("dataset/gifts_"+str(df.n_children)+".csv", dtype=np.int32, delimiter=",")
    wishlist = np.loadtxt("dataset/wishlist_"+str(df.n_children)+".csv", dtype=np.int32, delimiter=",")
    fitlist = np.asarray([fitness(individual, wishlist, gifts) for individual in generation])
    
    if not os.path.exists('outputs/'+df.configs):
        os.makedirs('outputs/'+df.configs)
    with open('outputs/'+df.configs+'/averages.txt','a') as f:
        f.write(str(np.average(fitlist))+'\n')
    with open('outputs/'+df.configs+'/maxs.txt','a') as f:
        f.write(str(np.max(fitlist))+'\n')
    with open('outputs/'+df.configs+'/mins.txt','a') as f:
        f.write(str(np.min(fitlist))+'\n')
    
    fitlist = fitlist.clip(min=0)
    fitprob = fitlist / np.sum(fitlist)
    
    indexes = np.random.choice(df.population_size,df.population_size,p=fitprob)
    
    new_generation = generation[indexes]
    fitlist = np.asarray([fitness(individual, wishlist, gifts) for individual in new_generation])
    
    max_index = np.argmax(fitlist)
    new_generation[0], new_generation[max_index] = new_generation[max_index], new_generation[0]


    return new_generation, fitlist[max_index] 
