# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import math
from collections import Counter
import defines as df

def lcm(a, b):
    """Compute the lowest common multiple of a and b"""
    # in case of large numbers, using floor division
    return a * b // math.gcd(a, b)

def avg_normalized_happiness(pred, child_pref, gift_pref):
    
    # check if number of each gift exceeds 1
    gift_counts = Counter(elem for elem in pred)
    for count in gift_counts.values():
        assert count <= df.gift_quantity

    # check if df.n_triplets have the same gift
    for t1 in np.arange(0,df.n_triplets,3):
        triplet1 = pred[t1]
        triplet2 = pred[t1+1]
        triplet3 = pred[t1+2]
        # print(t1, triplet1, triplet2, triplet3)
        assert triplet1 == triplet2 and triplet2 == triplet3
                
    # check if df.n_twins have the same gift
    for t1 in np.arange(df.n_triplets,df.n_triplets+df.n_twins,2):
        twin1 = pred[t1]
        twin2 = pred[t1+1]
        # print(t1)
        assert twin1 == twin2

    max_child_happiness = df.n_wishlist * df.ratio_child_happiness
    max_gift_happiness = df.n_children * df.ratio_gift_happiness
    total_child_happiness = 0
    total_gift_happiness = np.zeros(df.n_gift_types)
    
    for i, row in enumerate(pred):
        child_id = i
        gift_id = row
        
        # check if child_id and gift_id exist
        assert child_id < df.n_children
        assert gift_id < df.n_gift_types
        assert child_id >= 0 
        assert gift_id >= 0
        child_happiness = (df.n_wishlist - np.where(gift_pref[child_id]==gift_id)[0]) * df.ratio_child_happiness
        if not child_happiness:
            child_happiness = -1

        gift_happiness = ( df.n_children - np.where(child_pref[gift_id]==child_id)[0]) * df.ratio_gift_happiness
        if not gift_happiness:
            gift_happiness = -1

        total_child_happiness += child_happiness
        total_gift_happiness[gift_id] += gift_happiness
    
    # print('normalized child happiness=',float(total_child_happiness)/(float(df.n_children)*float(max_child_happiness)) , \
        # ', normalized gift happiness',np.mean(total_gift_happiness) / float(max_gift_happiness*df.gift_quantity))

    # to avoid float rounding error
    # find common denominator
    # NOTE: I used this code to experiment different parameters, so it was necessary to get the multiplier
    # Note: You should hard-code the multipler to speed up, now that the parameters are finalized
    denominator1 = df.n_children*max_child_happiness
    denominator2 = df.gift_quantity*max_gift_happiness*df.n_gift_types
    common_denom = lcm(denominator1, denominator2)
    multiplier = common_denom / denominator1

    # # usually denom1 > demon2
    return float(math.pow(total_child_happiness*multiplier,3) + math.pow(np.sum(total_gift_happiness),3)) / float(math.pow(common_denom,3))
    # return math.pow(float(total_child_happiness)/(float(df.n_children)*float(max_child_happiness)),2) + math.pow(np.mean(total_gift_happiness) / float(max_gift_happiness*1),2)

# random_sub = pd.read_csv('../input/sample_submission_random_v2.csv').values.tolist()
# print(avg_normalized_happiness(random_sub, child_pref, gift_pref))