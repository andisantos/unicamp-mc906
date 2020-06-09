import numpy as np
import defines as df

child_wishlist = np.asarray([np.random.choice(df.n_gift_types, df.n_wishlist, replace=False) for child in range(df.n_children)])
np.savetxt("dataset/wishlist_600.csv", child_wishlist, delimiter=",")
print(child_wishlist)
print()

gift_priority = np.asarray([np.random.choice(df.n_children, df.n_children, replace=False) for gift in range(df.n_gift_types)])
np.savetxt("dataset/gifts_600.csv", gift_priority, delimiter=",")
print(gift_priority)
