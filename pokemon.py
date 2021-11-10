import random
import requests



def get_random_number():
    random_number = random.randint(1, 151)
    return random_number






def random_pokemon():
    pokemon_number = random.randint(1, 151)
    url = 'https://pokeapi.co/api/v2/pokemon/{}/'.format(pokemon_number) 
    response = requests.get(url)
    pokemon = response.json()
    pokemon_dict = {
    'name': pokemon['name'], 'id': pokemon['id'],
    'height': pokemon['height'], 'weight': pokemon['weight'],
    }
    return pokemon_dict

def run():
    my_pokemon = random_pokemon()
    print('You were given {}'.format(my_pokemon['name']))
    stat_choice = input('Which stat do you want to use? (id, height, weight) ')
    opponent_pokemon = random_pokemon()
    print('The opponent chose {}'.format(opponent_pokemon['name']))
    my_stat = my_pokemon[stat_choice] 
    opponent_stat = opponent_pokemon[stat_choice]
    if my_stat > opponent_stat:
        print("You win!")
    elif my_stat < opponent_stat:
        print("You lose!")
    else:
        print("Try again")

run()