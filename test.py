import re
import json

with open('shanties_bs4_2.json', 'r') as fp:
    shanties_new = json.load(fp)

new_shanties = []

for name, lyrics in shanties_new.items():
    if not lyrics:
        continue
    if name > "Banks of the Sacramento":
        new_shanties.append({'title': name, 'lyrics': lyrics[:(len(lyrics)//2)]})
    else:
        new_shanties.append({'title': name, 'lyrics': lyrics})

with open('shanties_bs4_2_new.json', 'w') as fp:
    json.dump(new_shanties, fp)
