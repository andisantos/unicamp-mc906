import numpy as np
import defines as df

child_wishlist = np.asarray([np.random.choice(df.n_gift_types, df.n_wishlist, replace=False) for child in range(df.n_children)])
np.savetxt("dataset/wishlist_"+str(df.n_children)+".csv", child_wishlist, delimiter=",")
print(child_wishlist)
print()

gift_priority = np.asarray([np.random.choice(df.n_gift_types, df.n_gift_types, replace=False) for child in range(df.n_children)])
np.savetxt("dataset/gifts_"+str(df.n_children)+".csv", gift_priority, delimiter=",")
print(gift_priority)
