from pokemontcgsdk import Card

import os
import requests

def get_type(cards): 
    types = [card.types[0] for card in cards]

    return max(set(types), key = types.count)

#os.mkdir("./dataset", 0o755)
for i in range(873, 894):
    print("Getting cards for Pokemon " + str(i))

    cards = Card.where(nationalPokedexNumber=i, supertype='pokemon')

    if (len(cards) == 0):
        continue

    pokemon_type = get_type(cards)
    pokemon_path = "./dataset/"+pokemon_type

    print("- Got "+cards[0].name+" of type "+pokemon_type)
    print("- Got "+str(len(cards))+" cards for it, downloading images...")

    try:
        os.mkdir(pokemon_path, 0o755)
    except:
        pass

    for card in cards:
        r = requests.get(card.image_url, allow_redirects=True)
        open(pokemon_path+"/"+card.id+".png", 'wb').write(r.content)
