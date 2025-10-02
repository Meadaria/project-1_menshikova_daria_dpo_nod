from labyrinth_game.constants import ROOMS

def describe_current_room(game_state):
    """Функция описания комнаты"""
    current_room_name  = game_state['current_room']
    room_data =  ROOMS.get(current_room_name)
    current_items = game_state['room_items'][current_room_name]

    print(f"== {current_room_name.upper()} ==")
    print(f"{room_data['description']}")
    print(f"Выходы: {', '.join(room_data['exits'].keys())}")
    
    if current_items:
        print(f"Предметы в комнате: {', '.join(current_items)}")
    if room_data['puzzle']:
        if current_room_name not in game_state['solved_puzzles']:
            print(f"Кажется, здесь есть загадка (используйте команду solve).") 

def solve_puzzle(game_state):
    '''Функция решения загадок.'''
    room_data =  ROOMS.get(game_state['current_room'])
    current_room_name  = game_state['current_room']

    if room_data['puzzle'] is not None:
        print(room_data['puzzle'][0])
        answer = input("Ваш ответ: ")
        if answer == room_data['puzzle'][1]:
            print('Ну, это победа')
            game_state['solved_puzzles'].append(current_room_name)
            game_state['reward'] +=1
        else:
            print('Неверно. Попробуйте снова.')
    else:
        print("Загадок здесь нет.")

def attempt_open_treasure(game_state):
    '''Условие победы'''
    room_data =  ROOMS.get(game_state['current_room'])
    current_room = game_state['current_room']

    if 'treasure_chest' not in game_state['room_items']:
        print("Сундук уже открыт или отсутствует.")
        return
    if 'treasure_chest' in game_state['player_inventory']:
        if 'rusty_key' in game_state['player_inventory']:
            print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
            game_state['room_items'][current_room].remove('treasure_chest')
            game_state['game_over'] = True
        else:
            print("Ключа нет, но на сундуке есть код. Попробкешь решить? (да/нет)")
            answer = input('Да/нет: ')
            if answer.lower() == 'да':
                code = input()
                if code == room_data['puzzle'][1]:
                    print('Сокровище у Вас!')
                    game_state['game_over'] = True
                else:
                    print("Не подходит. Сундук все еще заперт")
            if answer.lower() == 'нет':
                print("Вы отступаете от сундука.")
            else:
                pass

def show_help():
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение") 
