import numpy as np
import defines as df
import fitness_function as ff
from operator import itemgetter
import sys
import os
import time

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
    ff_value = ff.avg_normalized_happiness(individual, wishlist, gifts)
    return ff_value

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

def get_first_triplet(index):
    # rounds down to a multiple of 3
    return 3 * (index // 3)

def get_first_twin(index):
    # if the list of twins starts at an odd index, then all twin pairs starts with an odd index as well
    # to find the first twin of a pair, an even index should become the previous odd
    # else we do the reverse
    if df.n_triplets % 2 == 1:
        return 2*((index+1)//2) - 1
    return 2 * (index // 2)

def cross_over(generation):
    cut_off = int(df.pass_threshold * df.population_size)

    for i in range(cut_off, df.population_size):
        pair = np.random.choice(cut_off, 2, replace=False)
        individual_1 = generation[pair[0]]
        individual_2 = generation[pair[1]]

        new_individual = np.zeros(df.n_children)
        counter = np.zeros(df.n_gift_types)

        # crossover triplets
        for j in range(0, df.n_triplets, 6):
            if counter[individual_1[j]] <= df.gift_quantity - 3:
                new_individual[j:j+3] = individual_1[j]
                counter[individual_1[j]] += 3
            elif counter[individual_2[j]] <= df.gift_quantity - 3:
                new_individual[j:j+3] = individual_2[j]
                counter[individual_2[j]] += 3
            else:
                gift = np.where(counter <= df.gift_quantity - 3)[0][0]
                new_individual[j:j+3] = gift
                counter[gift] += 3
        for j in range(3, df.n_triplets, 6):
            if counter[individual_2[j]] <= df.gift_quantity - 3:
                new_individual[j:j+3] = individual_2[j]
                counter[individual_2[j]] += 3
            elif counter[individual_1[j]] <= df.gift_quantity - 3:
                new_individual[j:j+3] = individual_1[j]
                counter[individual_1[j]] += 3
            else:
                gift = np.where(counter <= df.gift_quantity - 3)[0][0]
                new_individual[j:j+3] = gift
                counter[gift] += 3

        # crossover twins
        for j in range(df.n_triplets, df.n_triplets+df.n_twins, 4):
            if counter[individual_1[j]] <= df.gift_quantity - 2:
                new_individual[j:j+2] = individual_1[j]
                counter[individual_1[j]] += 2
            elif counter[individual_2[j]] <= df.gift_quantity - 2:
                new_individual[j:j+2] = individual_2[j]
                counter[individual_2[j]] += 2
            else:
                gift = np.where(counter <= df.gift_quantity - 2)[0][0]
                new_individual[j:j+2] = gift
                counter[gift] += 2
        for j in range(df.n_triplets+2, df.n_triplets+df.n_twins, 4):
            if counter[individual_2[j]] <= df.gift_quantity - 2:
                new_individual[j:j+2] = individual_2[j]
                counter[individual_2[j]] += 2
            elif counter[individual_1[j]] <= df.gift_quantity - 2:
                new_individual[j:j+2] = individual_1[j]
                counter[individual_1[j]] += 2
            else:
                gift = np.where(counter <= df.gift_quantity - 2)[0][0]
                new_individual[j:j+2] = gift
                counter[gift] += 2

        # crossover only-child
        for j in range(df.n_triplets+df.n_twins, df.n_children, 2):
            if counter[individual_1[j]] <= df.gift_quantity - 1:
                new_individual[j] = individual_1[j]
                counter[individual_1[j]] += 1
            elif counter[individual_2[j]] <= df.gift_quantity - 1:
                new_individual[j] = individual_2[j]
                counter[individual_2[j]] += 1
            else:
                gift = np.where(counter <= df.gift_quantity - 1)[0][0]
                new_individual[j] = gift
                counter[gift] += 1
        for j in range(df.n_triplets+df.n_twins+1, df.n_children, 2):
            if counter[individual_2[j]] <= df.gift_quantity - 1:
                new_individual[j] = individual_2[j]
                counter[individual_2[j]] += 1
            elif counter[individual_1[j]] <= df.gift_quantity - 1:
                new_individual[j] = individual_1[j]
                counter[individual_1[j]] += 1
            else:
                gift = np.where(counter <= df.gift_quantity - 1)[0][0]
                new_individual[j] = gift
                counter[gift] += 1

        generation[i] = new_individual

    return generation


def mutation(current_generation):
    cut_off = int(df.pass_threshold * df.population_size)

    # for each individual to be mutated(?)
    for individual in range(cut_off,df.population_size):
        modified_count = 0

        while modified_count < df.mutation_rate*df.n_children:
            while True:
                random_gifts = np.random.choice(df.n_gift_types, 2, replace=False)

                childs1 = np.where(current_generation[individual] == random_gifts[0])[0]
                childs2 = np.where(current_generation[individual] == random_gifts[1])[0]

                random_child = childs1[np.random.randint(0, len(childs1), 1)[0]]

                if random_child < df.n_triplets:
                    random_child = get_first_triplet(random_child)

                    if df.n_triplets <= childs2[0] < df.n_triplets+df.n_twins:
                        if childs2[2] >= df.n_triplets+df.n_twins:
                            current_generation[individual][childs2[0]] = random_gifts[0]
                            current_generation[individual][childs2[1]] = random_gifts[0]
                            current_generation[individual][childs2[2]] = random_gifts[0]
                        else:
                            continue
                    else:
                        current_generation[individual][childs2[0]] = random_gifts[0]
                        current_generation[individual][childs2[1]] = random_gifts[0]
                        current_generation[individual][childs2[2]] = random_gifts[0]

                    current_generation[individual][random_child:random_child+3] = random_gifts[1]
                    modified_count += 6
                elif df.n_triplets <= random_child < df.n_triplets+df.n_twins:
                    random_child = get_first_twin(random_child)

                    if childs2[0] >= df.n_triplets:
                        current_generation[individual][childs2[0]] = random_gifts[0]
                        current_generation[individual][childs2[1]] = random_gifts[0]
                    else:
                        continue

                    current_generation[individual][random_child:random_child+2] = random_gifts[1]
                    modified_count += 4
                else:
                    if childs2[0] >= df.n_triplets+df.n_twins:
                        current_generation[individual][childs2[0]] = random_gifts[0]
                    else:
                        continue

                    current_generation[individual][random_child] = random_gifts[1]
                    modified_count += 2

                break

    return current_generation

if __name__ == "__main__":
    print("Triplets:", df.n_triplets)
    print("Twins:", df.n_twins)
    print("Only:", df.n_children-df.n_twins-df.n_triplets)

    current_generation = create_initial_population()
    start = time.time()
    for i in range(df.max_generations):
        print('Geração ', i)
        current_generation = rank_fitness(current_generation)
        current_generation = cross_over(current_generation)
        current_generation = mutation(current_generation)

    current_generation = rank_fitness(current_generation)
    print(current_generation[0])
    time_elapsed = time.time() - start
    print("AVG TIME ELAPSED: {0}".format(str(time_elapsed/df.max_generations)))
