import numpy as np
import defines as df
from operator import itemgetter
import sys
import os
import time

import mutation as mutation
import crossover as crossover

def create_initial_population():
    solutions = np.zeros((df.population_size, df.n_children), dtype=np.int32)
    for i in range(df.population_size):
        available_gifts = np.full(df.n_gift_types, df.gift_quantity)

        for child in range(0, df.n_triplets, 3):
            possible_indexes = np.where(available_gifts >= 3)[0]
            random_index = np.random.randint(0, len(possible_indexes), 1)[0]
            index = possible_indexes[random_index]

            available_gifts[index] -= 3
            solutions[i][child:child+3] = int(index)

        for child in range(df.n_triplets, df.n_triplets+df.n_twins, 2):
            possible_indexes = np.where(available_gifts >= 2)[0]
            random_index = np.random.randint(0, len(possible_indexes), 1)[0]
            index = possible_indexes[random_index]

            available_gifts[index] -= 2
            solutions[i][child:child+2] = int(index)

        for child in range(df.n_triplets+df.n_twins, df.n_children):
            possible_indexes = np.where(available_gifts >= 1)[0]
            random_index = np.random.randint(0, len(possible_indexes), 1)[0]
            index = possible_indexes[random_index]

            available_gifts[index] -= 1
            solutions[i][child] = int(index)

    return solutions

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

if __name__ == "__main__":
    print("Triplets:", df.n_triplets)
    print("Twins:", df.n_twins)
    print("Only:", df.n_children-df.n_twins-df.n_triplets)

    current_generation = create_initial_population()
    start = time.time()
    for i in range(df.max_generations):
        print('Geração ', i)
        current_generation = rank_fitness(current_generation)
        current_generation = crossover.uniform_cross_over(current_generation)
        # current_generation = crossover.single_point_cross_over(current_generation)
        current_generation = mutation.mutation(current_generation)

    current_generation = rank_fitness(current_generation)
    print(current_generation[0])
    time_elapsed = time.time() - start
    print("AVG TIME ELAPSED: {0}".format(str(time_elapsed/df.max_generations)))
