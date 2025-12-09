

#NOT FINISHED
# Les templates d'attack sont isolable ligne 41
# il faut en récupérer l'attaque et la sauvegarder (récupérer le nom fr dans les fichier "traduction")

import json

LOC = './'

GAMEMASTER_FILENAME = LOC + 'latest.json'
CHARGE_MOVES_FILENAME = 'moves_charge_new.json'
FAST_MOVES_FILENAME = 'moves_fast_new.json'

MOVES_FAST = []
MOVES_CHARGE = []


def save_fast_move(raw_data: dict):
    pass
def save_charge_move(raw_data: dict):
    pass




def main():
    data = []

    # Get data from the gamemaster file
    with open(GAMEMASTER_FILENAME, 'r') as file:
        data = json.load(file)

    print(len(data)) # 14237

    # "templateId": "COMBAT_V
    raw_moves_fast = []
    raw_moves_charge = []

    for template in data:
        id: str = template['templateId']
        if id.startswith('COMBAT_V'):
            if id.endswith('_FAST'):
                raw_moves_fast.append(template)
            else:
                raw_moves_charge.append(template)

    for move in raw_moves_fast:
        print(json.dumps(move, indent=4, sort_keys=False, ensure_ascii=False))

    print(len(raw_moves_fast)) # 80
    print(len(raw_moves_charge)) # 221





if __name__ == '__main__':
    main()
    print('\nProg end.')



#SAVE LIST/DICT IN A FILE
# with open(file_name, "w") as file:
#     json.dump(data, file, indent=4)
