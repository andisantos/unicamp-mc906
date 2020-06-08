import numpy as np
import pandas as pd

n_children = 600
n_gifts = n_children
n_wishlist = 8

# Twins and triplets should get the same gift, even if they don't want the same one :(
n_triplets = 0.005*n_children
n_twins = 0.04*n_children
n_only_child = n_children - n_twins - n_triplets

child_wishlist = np.asarray([np.random.choice(n_gifts, n_wishlist, replace=False) for child in range(n_children)])
np.savetxt("dataset/wishlist_600.csv", child_wishlist, delimiter=",")
print(child_wishlist)
print()

gift_priority = np.asarray([np.random.choice(n_children, n_children, replace=False) for gift in range(n_gifts)])
np.savetxt("dataset/gifts_600.csv", gift_priority, delimiter=",")
print(gift_priority)

#csv = np.loadtxt("wishlist.csv", dtype=np.int32, delimiter=",")
