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
