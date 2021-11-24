import random
import requests



def get_random_number_up_to_151():
    random_number = random.randint(1, 151)
    return random_number

def get_random_number(nb_min, nb_max):
    random_number = random.randint(nb_min, nb_max)
    return random_number

def get_number_of_round():
    number_of_round = random.randint(1, 5)
    return number_of_round

def select_pokemon():
    pokemons = []
    number_max = 5
    number_min = 2
    number_of_pokemon = get_random_number(number_min, number_max)
    for i in range(number_of_pokemon):
        pokemon = random_pokemon()
        pokemons.append(pokemon)
    print('Here the pokemons:')
    for i in range(len(pokemons)):
        print((i+1), pokemons[i]['name'])
    number_pokemon_chosen = int(input('Which Pokemon do you want to use?\nSelect a number: ')) - 1
    pokemon_chosen = pokemons[number_pokemon_chosen]
    return pokemon_chosen

def get_pokemon(number_id):
    url = 'https://pokeapi.co/api/v2/pokemon/{}/'.format(number_id)
    response = requests.get(url)
    pokemon = response.json()
    return pokemon


def random_pokemon():
    pokemon_number = random.randint(1, 151)
    url = 'https://pokeapi.co/api/v2/pokemon/{}/'.format(pokemon_number)
    response = requests.get(url)
    pokemon = response.json()
    pokemon_dict = {
    'name': pokemon['name'], 'id': pokemon['id'],
    'height': pokemon['height'], 'weight': pokemon['weight'],
    'type': pokemon['types'][0]['type']['name']
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
