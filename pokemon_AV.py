import random
import requests
import time

print("Welcome To Our Pokemon Game!")
print("\n")
time.sleep(1)


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
    max_nb_of_pokemon = 5
    min_nb_of_pokemon = 2
    number_of_pokemon = get_random_number(min_nb_of_pokemon, max_nb_of_pokemon)
    for i in range(number_of_pokemon):
        pokemon = random_pokemon()
        pokemons.append(pokemon)
    print('Here the pokemons to chose from:')
    for indice in range(len(pokemons)):
        print((indice+1), pokemons[indice]['name'])
    number_pokemon_chosen = int(
        input('Which Pokemon do you want to use?\nSelect a number: ')) - 1
    pokemon_chosen = pokemons[number_pokemon_chosen]
    return pokemon_chosen


def get_round():
    nb_min = 3
    nb_max = 5
    number_rounds = get_random_number(nb_min, nb_max)
    return number_rounds


def play(my_score, opponent_score):
    pokemon = select_pokemon()
    print("\n")
    stat_choice = input('Which stat do you want to use? (id, height, weight) ')
    time.sleep(1)
    opponent_pokemon = random_pokemon()
    print("\n")
    print('The opponent chose {}'.format(opponent_pokemon['name']))
    my_stat = pokemon[stat_choice]
    opponent_stat = opponent_pokemon[stat_choice]
    if my_stat > opponent_stat:
        print("\n")
        time.sleep(1)
        print("You win this round!")
        print("\n")
        my_score += 1
        return my_score, opponent_score
    elif my_stat < opponent_stat:
        print("\n")
        print("You lose this round!")
        print("\n")
        opponent_score += 1
        return my_score, opponent_score
    else:
        print("Null")
        return my_score, opponent_score


def run():
    player_name = input('What is your name?')
    print("\n")
    number_rounds = get_round()
    time.sleep(1)
    print('There are {} rounds'.format(number_rounds))
    print("\n")
    player_score = 0
    opponent_score = 0
    for i in range(number_rounds):
        player_score, opponent_score = play(player_score, opponent_score)
    if player_score > opponent_score:
        print("\n")
        print("You won the game!")
        store_player_score_into_file(player_name, player_score)
    elif player_score < opponent_score:
        print("You lost the game!")
    else:
        time.sleep(1)
        print("Try again")


def store_player_score_into_file(player_name, player_score):
    f = open("score_pokemon_game.txt", "a")
    f.write(player_name + ": " + str(player_score))
    f.write("\n")
    f.close()


def get_winner(my_stat, opponent_stat):
    if my_stat > opponent_stat:
        print("You win!")
    elif my_stat < opponent_stat:
        print("You lose!")
    else:
        print("Try again")


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


run()
