import re
import json

with open('shanties.json', 'r') as fp:
    shanties_new = json.load(fp)

new_shanties = []

for name, lyrics in shanties_new.items():
    if not lyrics:
        continue
    
    new_shanties.append({'title': name, 'lyrics': lyrics})

with open('shanties_new_format.json', 'w') as fp:
    json.dump(new_shanties, fp)
