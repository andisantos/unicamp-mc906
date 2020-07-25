from pokemontcgsdk import Card

import os
import requests

os.mkdir("./dataset", 0o755);
for i in range(1, 152):
    cards = Card.where(nationalPokedexNumber=i, supertype='pokemon')
    pokemon_path = "./dataset/"+str(i)

    os.mkdir(pokemon_path, 0o755);

    for j, card in enumerate(cards):
        r = requests.get(card.image_url, allow_redirects=True)
        open(pokemon_path+"/"+str(j)+".png", 'wb').write(r.content)
