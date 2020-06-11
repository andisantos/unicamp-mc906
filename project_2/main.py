import numpy as np
import defines as df
import fitness_function as ff
from operator import itemgetter
import sys

def create_initial_population():
    solutions = np.asarray([np.random.choice(df.n_gift_types, df.n_children, replace=False) for _ in range(df.population_size)])
    
    for solution in solutions:
        for i in range(0, df.n_triplets, 3):
            solution[i:i+3] = solution[i]
        for i in range(df.n_triplets, df.n_triplets+df.n_twins, 2):
            solution[i:i+2] = solution[i]

    return solutions

def fitness(individual, wishlist, gifts):
    ff_value = ff.avg_normalized_happiness(individual, wishlist, gifts)
    print("INDIVIDUAL AVG = ", ff_value)
    return ff_value

def rank_fitness(generation):
    gifts = np.loadtxt("dataset/gifts_600.csv", dtype=np.int32, delimiter=",")
    wishlist = np.loadtxt("dataset/wishlist_600.csv", dtype=np.int32, delimiter=",")

    fitlist = np.asarray([fitness(individual, wishlist, gifts) for individual in generation])
    np.set_printoptions(threshold=sys.maxsize)
    generation = np.asarray([x for _, x in sorted(zip(fitlist, generation), key=itemgetter(0), reverse=True)])
    return generation

def cross_over(generation):
    cut_off = int(df.pass_threshold * df.population_size)

    for i in range(cut_off, df.population_size):
        pair = np.random.choice(cut_off, 2, replace=False)
        individual_1 = generation[pair[0]]
        individual_2 = generation[pair[1]]

        new_individual = np.zeros(df.n_children)

        # crossover triplets
        for j in range(0, df.n_triplets, 6):
            new_individual[j:j+3] = individual_1[j]
        for j in range(3, df.n_triplets, 6):
            new_individual[j:j+3] = individual_2[j]

        # crossover twins
        for j in range(df.n_triplets, df.n_triplets+df.n_twins, 4):
            new_individual[j:j+2] = individual_1[j]
        for j in range(df.n_triplets+2, df.n_triplets+df.n_twins, 4):
            new_individual[j:j+2] = individual_2[j]

        # crossover only-child
        for j in range(df.n_triplets+df.n_twins, df.n_children, 2):
            new_individual[j] = individual_1[j]
        for j in range(df.n_triplets+df.n_twins+1, df.n_children, 2):
            new_individual[j] = individual_2[j]

        while 1:
            # count the number of gifts of each type
            gift_counts = ff.Counter(elem for elem in new_individual)

            if all(count <= df.gift_quantity for count in gift_counts.values()):
                break

            for gift in gift_counts:
                if gift_counts[gift] > df.gift_quantity:
                    index = np.where(new_individual == gift)[0][-1]

                    if index < df.n_triplets:
                        # rounds down to a multiple of 3
                        first_triplet = 3 * (index // 3)

                        # if triplet group is a even group it came from individual 1, so we changed to the individual 2
                        # else we do reverse
                        if (index // 3) % 2 == 0:
                            new_individual[first_triplet:first_triplet+3] = individual_2[first_triplet]
                        else:
                            new_individual[first_triplet:first_triplet+3] = individual_1[first_triplet]

                    elif df.n_triplets <= index < df.n_triplets+df.n_twins:

                        # if the list of twins starts at an odd index, then all twin pairs starts with an odd index as well
                        # to find the first twin of a pair, an even index should become the previous odd
                        # else we do the reverse
                        if df.n_triplets % 2 == 1:
                            first_twin = 2*((index+1)//2) - 1
                        else:
                            first_twin = 2 * (index // 2)

                        if (index // 2) % 2 == 0:
                            new_individual[first_twin:first_twin+2] = individual_2[first_twin]
                        else:
                            new_individual[first_twin:first_twin+2] = individual_1[first_twin]

                    else:
                        if index % 2 == 0:
                            new_individual[index] = individual_2[index]
                        else:
                            new_individual[index] = individual_1[index]

        generation[i] = new_individual

    return generation


if __name__ == "__main__":

    current_generation = create_initial_population()

    for i in range(df.max_generations):
        current_generation = rank_fitness(current_generation)
        current_generation = cross_over(current_generation)
        # current_generation = mutation(current_generation)

