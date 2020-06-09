import numpy as np
import defines as df
import fitness_function as ff

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
    generation = np.asarray([x for _, x in sorted(zip(fitlist, generation), reverse=True)])
    return generation


if __name__ == "__main__":

    current_generation = create_initial_population()

    for i in range(df.max_generations):
        current_generation = rank_fitness(current_generation)
        # current_generation = cross_over(current_generation)
        # current_generation = mutation(current_generation)

