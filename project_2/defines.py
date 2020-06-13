#
n_gift_types = 20

gift_quantity = n_gift_types
n_children = n_gift_types*gift_quantity
n_wishlist = 8

# twins and triplets should get the same gift, even if they don't want the same one :(
n_triplets = 3*int(0.005*n_children)
n_twins = 2*int(0.04*n_children)
n_only_child = n_children - n_twins - n_triplets

#
population_size = 100
mutation_rate = 0.05
max_generations = 1000
pass_threshold = 0.2

# defines for fitness_function
ratio_gift_happiness = 2
ratio_child_happiness = 2
