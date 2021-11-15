import csv
import random
import requests
import pandas as pd
import os.path
 

def run():
    data_from_api = get_data_from_HP_api()
    player_A = choose_character(data_from_api)
    player_B = select_random_character_computer(data_from_api)
    print("Your opponent is {}".format(player_B['name']))
    print("You are {}".format(player_A['name']))
    score_record = read_score()
    print("Let's fight!")
    play(player_A, player_B, score_record)

def play(player_A, player_B, score_record):
    if (player_A['wizard'] is False) and (player_B['wizard'] is False):
        print("Epic Fail, your are both moduls!")  
    else:
        continue_round = True
        while continue_round is True:
            player_A['life_point'], player_B['life_point'] = attack(player_A, player_B)
            continue_round = evaluate_life_point(player_A, player_B, score_record)

def evaluate_life_point(player_A, player_B, score_record):
    if (player_A['life_point'] <= 0) and (player_B['life_point'] > 0):
        print("Player B win")
        score_record.loc[score_record["name"]==player_B['name'], "score"] += 10
        score_record.to_csv("score_HP.csv", index=False)
        return False
    elif (player_A['life_point'] > 0) and (player_B['life_point'] <= 0):
        print("Player A win")
        score_record.loc[score_record["name"]==player_A['name'], "score"] += 10
        score_record.to_csv("score_HP.csv", index=False)
        return False
    elif (player_A['life_point'] <= 0) and (player_B['life_point'] <= 0):
        print("Epic Fail!\n Your are both lose.")
        return False
    else:
        return True

def attack(player_A, player_B):
    player_B['life_point'] = cast_a_spell(player_A, player_B)
    print("Player B life span {}".format(player_B['life_point']))
    print("Player opponent attacks!")
    player_A['life_point'] = computer_cast_spell(player_A, player_B)
    print("Player A life span {}".format(player_A['life_point']))
    return player_A['life_point'], player_B['life_point']

def cast_a_spell(player_attacking, player_attacked):
    print("Choose your attack\n")
    for spell in player_attacking['spells']:
        print(spell)
    spell_to_cast = input("which spell?\n")
    player_attacked['life_point'] = calculate_damage(spell_to_cast, player_attacked, player_attacking)
    return player_attacked['life_point']

def computer_cast_spell(player_attacked, player_attacking):
    if player_attacking['wizard'] is False:
        attacks = ["scream" ,'run away']
    else:
        attacks = ['CRUCIO', 'AVADA KEDAVRA' ,'EXPECTO PATRONUM', 
                   'IMPERIO', 'OBLIVIATE', 'BOMBARDA MAXIMA', 
                   'EXPELLIARMUS', 'SECTUMSEMPRA']
    random_attack = random.randint(0, len(attacks) - 1)
    attack = attacks[random_attack]
    player_attacked['life_point'] = calculate_damage(attack, player_attacked, player_attacking)
    return player_attacked['life_point']

def calculate_damage(attack, player_attacked, player_attacking):
    player_attacked['life_point'] = player_attacked['life_point'] - player_attacking['spells'][attack]
    return player_attacked['life_point']

def create_character_selection(data_from_api):
    characters = []
    number_of_characters = 3
    for i in range(number_of_characters):
        character = get_player(data_from_api)
        characters.append(character)
    return characters

def select_random_character_computer(data_from_api):
    characters = create_character_selection(data_from_api)
    random_number = random.randint(0, len(characters) - 1)
    character = characters[random_number]
    return character

def choose_character(data_from_api):
    characters = create_character_selection(data_from_api)
    print("Select your personage")
    for i in range(len(characters)):
        print(i+1, characters[i]['name'])
    character_number = int(input("Enter the character number \n")) - 1
    return characters[character_number]

def create_record_score(file_name):
    data_from_api = get_data_from_HP_api()
    rows = []
    header_score = ['name','score']
    for i in range(len(data_from_api)):
        name = data_from_api[i]['name']
        rows.append({'name':name, 'score':0})
    with open(file_name, 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header_score)
        writer.writeheader()
        writer.writerows(rows)
    
def read_score():
    file_name = 'score_HP.csv'
    if os.path.isfile(file_name) is False:
        create_record_score(file_name)
    score = pd.read_csv(file_name)
    return score

def get_data_from_HP_api():
    url = 'http://hp-api.herokuapp.com/api/characters' 
    response = requests.get(url)
    data = response.json()
    return data

def get_player(data_from_api):
    number_characters = len(data_from_api)
    number_random_player = random.randint(0, number_characters)
    player = data_from_api[number_random_player]
    player_character = create_character(player)
    return player_character 

def create_character(player):
    if player['wizard'] is False:
        life_point = 5
        spells = {"scream":0 ,'run away':0}
    else:
        spells = {'CRUCIO': 1, 'AVADA KEDAVRA': 10 ,'EXPECTO PATRONUM': 3, 
            'IMPERIO': 4, 'OBLIVIATE': 4, 'BOMBARDA MAXIMA': 4, 
            'EXPELLIARMUS': 2, 'SECTUMSEMPRA': 1}
        if player['hogwartsStudent'] is True:
            life_point = random.randint(7, 20)
            if player['house'] == 'Gryffindor':
                life_point += 5
        elif player['hogwartsStaff']  is True:
            life_point = random.randint(7, 15)
        else:
            life_point = random.randint(3, 10)

    player_dict = {
    'name': player['name'], 'species': player['species'],
    'house': player['house'], 'wizard': player['wizard'],
    'hogwartsStudent': player['hogwartsStudent'], 'hogwartsStaff': player['hogwartsStaff'],
    'patronus': player['patronus'], 'life_point': life_point, 'spells' : spells
    }
    return player_dict


run()