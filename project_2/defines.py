# CHANGE THESE
n_gift_types = 20
population_size = 100
mutation_rate = 0.05
pass_threshold = 0.2
stop_by_generations = False
goal_fitness = 0.2

# DON'T CHANGE BELOW :)
gift_quantity = n_gift_types
n_children = n_gift_types*gift_quantity
n_wishlist = 8

# twins and triplets should get the same gift, even if they don't want the same one :(
n_triplets = 3*int(0.005*n_children)
n_twins = 2*int(0.04*n_children)
n_only_child = n_children - n_twins - n_triplets

max_generations = 2000

# defines for fitness_function
ratio_gift_happiness = 2
ratio_child_happiness = 2

# filename config
configs = str(n_gift_types)+'_'+str(population_size)+'_'+str(mutation_rate)+'_'+str(max_generations)+'_'+str(pass_threshold)
