import time
import numpy as np

import defines as df
import mutation
import crossover
import fitness_function as ff

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

if __name__ == "__main__":
    print("Triplets:", df.n_triplets)
    print("Twins:", df.n_twins)
    print("Only:", df.n_children-df.n_twins-df.n_triplets)

    current_generation = create_initial_population()
    start = time.time()

    if df.stop_by_generations:
        for i in range(df.max_generations):
            print('Geração ', i)
            current_generation, _ = ff.roulette_fitness(current_generation)
            current_generation = crossover.uniform_cross_over(current_generation)
            current_generation = mutation.mutation(current_generation)
        time_elapsed = time.time() - start
        print("AVG TIME ELAPSED: {0}".format(str(time_elapsed/df.max_generations)))
    else:
        current_fitness = 0
        i = 0
        while current_fitness < df.goal_fitness:
            print('Geração ', i)
            print('Fitness ', current_fitness)
            current_generation, current_fitness = ff.rank_fitness(current_generation)
            current_generation = crossover.uniform_cross_over(current_generation)
            current_generation = mutation.mutation(current_generation)
            i += 1
        time_elapsed = time.time() - start
        print("AVG TIME ELAPSED: {0}".format(str(time_elapsed/i)))
