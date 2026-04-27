#TO DO

import json


gamemaster_filename = 'latest.json'
pokemons_filename = 'pokemons.json'
moves_filename = 'moves.json'

traduction_charge_filename = 'traduction_charge.json'
traduction_fast_filename = 'traduction_fast.json'



def get_data_from_json(filename: str) -> list | dict:
    try:
        file = open(filename, 'r')
        data = json.loads(file.read())
        file.close()
    except:
        return []
    return data




def save_data_in_json(data, filename: str):
    file = open(filename, 'w')
    file.write(json.dumps(data, indent=4, ensure_ascii=False))
    file.close()

    #temp, write main keys
    file = open(f'KEYS_{filename}', 'w')

    if filename == pokemons_filename:
        for key, entry in data.items():
            file.write(key + '\n')
    else:
        for entry in data:
            file.write(entry['templateId'] + '\n')

    file.close()



def reformat_pokemon_entry(entry: dict) -> tuple[str, dict]:
    # raw data (only what i need)
    # {
    #     "templateId": "V0001_POKEMON_BULBASAUR",
    #     "data": {
    #         "templateId": "V0001_POKEMON_BULBASAUR",
    #         "pokemonSettings": {
    #             "pokemonId": "BULBASAUR",
    #             "type": "POKEMON_TYPE_GRASS",
    #             "type2": "POKEMON_TYPE_POISON",
    #             "stats": {
    #                 "baseStamina": 128,
    #                 "baseAttack": 118,
    #                 "baseDefense": 111
    #             },
    #             "quickMoves": [
    #                 "VINE_WHIP_FAST",
    #                 "TACKLE_FAST"
    #             ],
    #             "cinematicMoves": [
    #                 "SLUDGE_BOMB",
    #                 "SEED_BOMB",
    #                 "POWER_WHIP"
    #             ],
    #         }
    #     }
    # }


    # format to a more comprehensible form, and proper for dictionary usage
    # "V0001_POKEMON_BULBASAUR" : {
    #     "pokemonId": "BULBASAUR",
    #     "type": "POKEMON_TYPE_GRASS",
    #     "type2": "POKEMON_TYPE_POISON",
    #     "stats": {
    #         "baseStamina": 128,
    #         "baseAttack": 118,
    #         "baseDefense": 111
    #     },
    #     "quickMoves": [
    #         "VINE_WHIP_FAST",
    #         "TACKLE_FAST"
    #     ],
    #     "cinematicMoves": [
    #         "SLUDGE_BOMB",
    #         "SEED_BOMB",
    #         "POWER_WHIP"
    #     ],
    # }


    #tell if name is inside the id
    if entry['data']['pokemonSettings']['pokemonId'] not in entry['templateId']:
        if 'NIDORAN' not in entry['templateId']:
            print(entry['templateId'])
            print(entry['data']['pokemonSettings']['pokemonId'])
            print('name is different then id')
            input('...')


    key = entry['templateId']
    new_entry = {}

    new_entry['pokemonId'] = entry['data']['pokemonSettings']['pokemonId']

    new_entry['type'] = entry['data']['pokemonSettings']['type']

    try:
        new_entry['type2'] = entry['data']['pokemonSettings']['type2']
    except:
        new_entry['type2'] = new_entry['type']

    new_entry['stats'] = entry['data']['pokemonSettings']['stats']

    try:
        new_entry['quickMoves'] = entry['data']['pokemonSettings']['quickMoves']
    except:
        new_entry['quickMoves'] = []

    try:
        new_entry['cinematicMoves'] = entry['data']['pokemonSettings']['cinematicMoves']
    except:
        new_entry['cinematicMoves'] = []

    return key, new_entry




def extract(gamemaster: list[dict]):
    pokemons: dict = {}
    moves: list[dict] = []
    for entry in gamemaster:
        templateId = entry['templateId'].lower()

        if templateId[0] != 'v':
            continue


        if 'pokemon' in templateId:
            #to ignore
            if 'home_form_reversion' in templateId:
                continue
            if 'giratina_home_reversion' in templateId:
                continue
            if 'seeker_pokemon_rewards' in templateId:
                continue


            # if '_NORMAL'.lower() not in templateId: #_NORMAL _ALOLA _GALARIAN _HISUIAN _PALDEA
            #     continue

            if False:
                key, new_entry = shorten_pokemon_entry(entry)
                pokemons[key] = new_entry
            else:
                try:
                    key, new_entry = reformat_pokemon_entry(entry)
                    #tell if key exists
                    if key in pokemons.keys():
                        print("waitwaitwait, key already exists")
                        print(key)
                        input('...')
                    pokemons[key] = new_entry
                except:
                    print(f'error at {templateId}')
                    input('...')


        # if 'move' in templateId:
        #     moves.append(entry)
        

    
    return pokemons, moves




def are_same(dictA: dict, dictB: dict):
    return dictA == dictB



#remove duplicates, and change key for the pokemon name
def reduce_pokemons(pokemons: dict):
    new_pokemons: dict = {}

    for key, value in pokemons.items():
        # print(f'reduce_pokemons(): {key}')
        name = value['pokemonId']

        #add if non existant yet        
        existing_value = new_pokemons.get(name)
        if not existing_value:
            value['pokemonId'] = key
            new_pokemons[name] = value
            # new_pokemons[name]['pokemonId'] = key
            continue
        
        existing_value = existing_value.copy()

        #here, an item is already register with this pokemon's name
        
        #reset existing_value to it's first state
        existing_key = existing_value['pokemonId']
        existing_value['pokemonId'] = name

        #compare
        if existing_value == value:
            # if '_NORMAL' in key:
            #     continue
            # print('already registered')
            # print(key)
            # print(value)
            # input('...')
            continue

        #whole new value
        appendice = key.replace(existing_key, '')
        if not appendice:
            appendice = existing_key.replace(key, '')
        
        name = name + appendice

        new_pokemons[name] = value
        new_pokemons[name]['pokemonId'] = key
    
    return new_pokemons




def add_not_found_moves(move: str):
    file = open('not_found_moves.txt', 'a')
    file.write(move + '\n')
    file.close()




def traduct_moves(pokemons: dict):
    total_moves_checked = 0
    total_moves_not_found = 0
    total_moves_modification = 0
    all_fast_moves: dict = get_data_from_json(traduction_fast_filename)
    all_charge_moves: dict = get_data_from_json(traduction_charge_filename)

    for key, entry in pokemons.items():
        untraducted_fast_moves = entry['quickMoves']
        untraducted_charge_moves = entry['cinematicMoves']

        new_moves = []
        for move in untraducted_fast_moves:
            total_moves_checked += 1

            #TO DO maybe be careful about the type, maybe i'll take care of this
            if len(move) > 5 and move[-5:] == '_FAST':
                move = move.replace('_FAST', '')

            traduction = all_fast_moves.get(move.lower())
            if traduction is None:
                total_moves_not_found += 1
                add_not_found_moves(f'{move} ({key})')
                # print(f'traduction not found for : {move} ({key})')
                continue
            # new_moves.append(f'{move} -> {traduction}')
            new_moves.append(traduction)
        entry['quickMoves'] = new_moves

        new_moves = []
        for move in untraducted_charge_moves:
            total_moves_checked += 1
            if  move in [406, 407]: #gamemaster file format mistake
                move = 'AURA_WHEEL'
                total_moves_modification += 1
            if 'WEATHER_BALL' in move: #multi-element versions
                move = 'WEATHER_BALL'
                total_moves_modification += 1
            if move == 'VICE_GRIP': #misspell
                move = 'VISE_GRIP'
                total_moves_modification += 1
            if move == 'FUTURESIGHT': #typo
                move = 'FUTURE_SIGHT'
                total_moves_modification += 1
            if move == 'SUPER_POWER': #typo
                move = 'SUPERPOWER'
                total_moves_modification += 1
            if move == 'PYROBALL': #typo
                move = 'PYRO_BALL'
                total_moves_modification += 1

            traduction = all_charge_moves.get(move.lower())
            if traduction is None:
                total_moves_not_found += 1
                add_not_found_moves(f'{move} ({key})')
                # print(f'traduction not found for : {move} ({key})')
                continue
            # new_moves.append(f'{move} -> {traduction}')
            new_moves.append(traduction)
        entry['cinematicMoves'] = new_moves
    
    print('traduct_moves()')
    print(f'Not found: {total_moves_not_found}/{total_moves_checked}')
    print(f'Modified: {total_moves_modification}')
    if total_moves_not_found > 0:
        print('Check [not_found_moves.txt]')
        

            
        












def main():
    gamemaster: list[dict] = None
    pokemons: dict = None
    moves: list[dict] = None

    gamemaster = get_data_from_json(gamemaster_filename)
    # pokemons = get_data_from_json(pokemons_filename)
    # moves = get_data_from_json(moves_filename)

    pokemons, moves = extract(gamemaster)
    pokemons = reduce_pokemons(pokemons)
    traduct_moves(pokemons)

    save_data_in_json(pokemons, pokemons_filename)
    save_data_in_json(moves, moves_filename)

    # print(gamemaster)
    # print(type(gamemaster))
    # print(len(gamemaster))




if __name__ == '__main__':
    main()
    print('\n\nPROG END.')





