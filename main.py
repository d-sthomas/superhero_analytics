import requests
import json
import numpy as np
import math
import matplotlib.pyplot as plt
import re

api_key = '274269408311698	'
base_url = f"https://superheroapi.com/api/{api_key}"
character_db = []

# returns name and full name of character given id
def id_to_name(param_id):
    for character in character_db:
        id = character['id']
        if id == param_id:
            name = character['name']
            full_name = character['biography']['full-name']
            return {'name': name, 'full name': full_name}

# creates database of characters
def get_characters():
    # 731 characters in api
    for i in range(1, 732):
        character_url = f"{base_url}/{i}"
        response = requests.get(character_url)
        data = json.loads(response.text)
        alignment = data['biography']['alignment']
        if alignment != 'bad':
            character_db.append(data)

# orders characters by average powerstat (descending order)
def ranking_powerstat():
    stats_avg = {}
    for character in character_db:
        id = character['id']
        # checks if each value is null before adding it to calculation
        intelligence = 0 if character['powerstats']['intelligence'] == 'null' else int(character['powerstats']['intelligence'])
        strength = 0 if character['powerstats']['strength'] == 'null' else int(character['powerstats']['strength'])
        speed = 0 if character['powerstats']['speed'] == 'null' else int(character['powerstats']['speed'])
        durability = 0 if character['powerstats']['durability'] == 'null' else int(character['powerstats']['durability'])
        power = 0 if character['powerstats']['power'] == 'null' else int(character['powerstats']['power'])
        combat = 0 if character['powerstats']['combat'] == 'null' else int(character['powerstats']['combat'])
        avg = np.average([intelligence, strength, speed, durability, power, combat])
        stats_avg[id] = avg

    # sorts character averages in descending order
    sorted_descending = dict(sorted(stats_avg.items(), key=lambda x:x[1], reverse=True))
    print(sorted_descending)
    return sorted_descending

# ranking powerstats by how common they are; a powerstat is counted if it's value is over 50
# ex. batman (id 70) has speed 27. speed is not one of his specializations
def most_common_powerstat():
    # 6 powerstats from api
    stats = {'intelligence': 0, 'strength': 0, 'speed': 0, 'durability': 0, 'power': 0, 'combat': 0}
    for character in character_db:
        if character['powerstats']['intelligence'] != 'null' and int(character['powerstats']['intelligence']) >= 50: stats['intelligence'] += 1
        if character['powerstats']['strength'] != 'null' and int(character['powerstats']['strength']) >= 50: stats['strength'] += 1
        if character['powerstats']['speed'] != 'null' and int(character['powerstats']['speed']) >= 50: stats['speed'] += 1
        if character['powerstats']['durability'] != 'null' and int(character['powerstats']['durability']) >= 50: stats['durability'] += 1
        if character['powerstats']['power'] != 'null' and int(character['powerstats']['power']) >= 50: stats['power'] += 1
        if character['powerstats']['combat'] != 'null' and int(character['powerstats']['combat']) >= 50: stats['combat'] += 1
        
    sorted_descending = dict(sorted(stats.items(), key=lambda x:x[1], reverse=True))
    powers = list(sorted_descending.keys())
    values = list(sorted_descending.values())

    plt.barh(powers, values)
    plt.ylabel("powerstats")
    plt.xlabel("amount of characters power appears in")
    plt.title("Ranking powerstats by appearance")
    plt.savefig('data/powerstats.png')

def largest_group():
    groups = get_group_sizes()
    print(groups)

    sorted_descending = dict(sorted(groups.items(), key=lambda x:x[1], reverse=True))
    largest_group = list(sorted_descending.keys())[0]
    size = list(sorted_descending.values())[0]
    print(f'The largest group is {largest_group} with {size} members')
    return {largest_group: size}

# some duplicates with spelling variations
def get_group_sizes():
    groups = {}

    for character in character_db:
        affiliations_string = character['connections']['group-affiliation']
        if affiliations_string == '-':
            if 'Solo' in groups: groups['Solo'] += 1
            else: groups['Solo'] = 1
        else:
            affiliations_string = affiliations_string.replace(';', ', ')
            affiliations_list = affiliations_string.split(',')
            for affiliation in affiliations_list:
                if ('former' and 'Former') not in affiliation:
                    affiliation = re.sub("[\(\[].*?[\)\]]", "", affiliation)
                    affiliation = affiliation.strip()
                    if affiliation in groups: groups[affiliation] += 1
                    else: groups[affiliation] = 1

    return groups
    

if __name__ == "__main__":
    get_characters()
    largest_group()
    ranking_powerstat()
    most_common_powerstat()