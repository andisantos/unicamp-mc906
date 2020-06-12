#
n_children = 600
n_gift_types = n_children
n_wishlist = 8

# twins and triplets should get the same gift, even if they don't want the same one :(
n_triplets = int(0.005*n_children)
n_twins = int(0.04*n_children)
n_only_child = n_children - n_twins - n_triplets

#
population_size = 100
mutation_rate = 0.05
max_generations = 20000
pass_threshold = 0.2

# defines for fitness_function
ratio_gift_happiness = 2
ratio_child_happiness = 2
gift_quantity = n_children
