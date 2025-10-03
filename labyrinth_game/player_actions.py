from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import describe_current_room, random_event


def show_inventory(game_state):
    '''Функция отображения инвентаря.'''
    if game_state['player_inventory']:
        print(f"Предметы в инвентаре: {', '.join(game_state['player_inventory'])}")
    else:
        print('Упс, кажется инветарь пуст')

def get_input(prompt="> "):
    '''Ввод пользователя.'''
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit" 
    
def move_player(game_state, direction):
    '''Функция перемещения'''
    room_data =  ROOMS.get(game_state['current_room'])

    if direction in room_data['exits']:
        if room_data['exits'][direction] == 'treasure_room':
            if 'rusty_key' in game_state['player_inventory']:
                print("Вы используете найденный ключ, " \
                "чтобы открыть путь в комнату сокровищ.")
                game_state['current_room'] = room_data['exits'][direction]
                game_state['steps_taken'] += 1
                random_event(game_state)
                describe_current_room(game_state)
            else:
                print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
        else:
            game_state['current_room'] = room_data['exits'][direction]
            game_state['steps_taken'] += 1
            random_event(game_state)
            describe_current_room(game_state)
    else:
        print("Нельзя пойти в этом направлении.")

def take_item(game_state, item_name):
    '''Функция взятия предмета.'''
    current_room = game_state['current_room']

    if item_name in game_state['room_items'][current_room]:
        game_state['player_inventory'].append(item_name)
        game_state['room_items'][current_room].remove(item_name)
        print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")

def use_item(game_state, item_name):
    '''Функция использования предметов. '''

    if item_name in game_state['player_inventory']:
        match item_name:
            case 'torch':
                print('Комнату озарил свет')
            case 'sword':
                print('Уверенность в себе увеличилась на 100')
            case 'bronze box':
                print('Шкатулка открывается. Вы получили ржавый ключ.')
                if 'rusty_key' not in game_state['player_inventory']:
                    game_state['player_inventory'].append('rusty_key')
                else:
                    pass
            case _:
                print('Какая-то странная фиговина, непонятно для чего нужна')
    else:
        print('У вас нет такого предмета.')


