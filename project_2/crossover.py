import defines as df
import numpy as np

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

def uniform_cross_over(generation):
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

def single_point_cross_over(generation):

    cut_off = int(df.pass_threshold * df.population_size)
    
    # cromossomes from 0 to single point index comes from indivudal_1
    # rest comes from individual_2
    single_point = df.n_children//2

    for i in range(1, df.population_size):
        pair = np.random.choice(cut_off, 2, replace=False)
        individual_1 = generation[pair[0]]
        individual_2 = generation[pair[1]]

        new_individual = np.zeros(df.n_children)
        counter = np.zeros(df.n_gift_types)

        # copy half gifts from individual 1
        for j in range(0, single_point):
            new_individual[j] = individual_1[j]
            counter[individual_1[j]] += 1

        modified_index = j
        # is possible that only part of the triplets were copied
        if (df.n_triplets % single_point) != 0:
            first_triplet = get_first_triplet(single_point-1)
            new_individual[first_triplet:first_triplet+3] = individual_1[j-1]

            # if only one was copied, two more gifts needs to be counted
            # otherwise only one
            if (single_point - first_triplet) == 2:
                counter[individual_1[j]] += 1
            else:
                counter[individual_1[j]] += 2

            modified_index = first_triplet + 3
        # same with twins
        elif (df.n_twins % single_point) != 0:
            first_twin = get_first_twin(single_point-1)
            new_individual[first_twin:first_twin+2] = individual_1

            counter[individual_1[j]] += 1
            modified_index = first_twin + 2

        # copy the rest of the gifts from individual 2, if possible
        for j in range(modified_index, df.n_children):
            # crossover triplets
            if j < df.n_triplets:
                if counter[individual_2[j]] <= df.n_gift_types - 3:
                    new_individual[j:j+3] = individual_2[j]
                    counter[individual_2[j]] += 3
                else:
                    gift = np.where(counter <= df.gift_quantity - 3)[0][0]
                    new_individual[j:j+3] = gift
                    counter[gift] += 3
            
            # crossover twins
            if df.n_triplets <= j < df.n_triplets+df.n_twins:
                if counter[individual_2[j]] <= df.n_gift_types - 2:
                    new_individual[j:j+2] = individual_2[j]
                    counter[individual_2[j]] += 2
                else:
                    gift = np.where(counter <= df.gift_quantity - 2)[0][0]
                    new_individual[j:j+2] = gift
                    counter[gift] += 2

            # crossover only-childe
            else:
                if counter[individual_2[j]] <= df.n_gift_types - 1:
                    new_individual[j] = individual_2[j]
                    counter[individual_2[j]] += 1
                else:
                    gift = np.where(counter <= df.gift_quantity - 1)[0][0]
                    new_individual[j] = gift
                    counter[gift] += 1

        generation[i] = new_individual

    return generation