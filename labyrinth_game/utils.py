import math

from labyrinth_game.constants import ROOMS

EVENT_PROBABILITY = 10
EVENT_TYPES = 3
DAMAGE_THRESHOLD = 3
MAX_DAMAGE = 9


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
            print("Кажется, здесь есть загадка (используйте команду solve).") 

def solve_puzzle(game_state):
    '''Функция решения загадок.'''
    room_data =  ROOMS.get(game_state['current_room'])
    current_room_name  = game_state['current_room']
    c_solved_puzzles = game_state['solved_puzzles']

    if room_data['puzzle'] is not None and current_room_name not in c_solved_puzzles:
        print(room_data['puzzle'][0])
        answer = input("Ваш ответ: ")
        correct_answer = str(room_data['puzzle'][1]).lower()

        alternative_answers = {
            '10': ['десять', 'ten'],
            '3' : ['три', 'three'],
            '5': ['пять', 'five'],
            '2520': ['две тысячи пятьсот двадцать'],
            'шаг шаг шаг': ['step step step', 'steps steps steps'],
        }

        is_correct = (answer == correct_answer or 
                     answer in alternative_answers.get(correct_answer, []))
        
        if is_correct:
            print('Правильно!')
            game_state['solved_puzzles'].append(current_room_name)
            game_state['reward'] +=1

            if current_room_name == 'hall':
                game_state['player_inventory'].append('treasure_key')
                print('Вы получили: treasure_key')
            elif current_room_name == 'library':
                game_state['player_inventory'].append('rusty_key')
                print('Вы получили: rusty_key')
            
        else:
            print('Неверно. Попробуйте снова.')
            if current_room_name == 'trap_room':
               trigger_trap(game_state)

    elif current_room_name in game_state['solved_puzzles']:
        print("Вы уже решили загадку в этой комнате.")

    else:
        print("Загадок здесь нет.")

def attempt_open_treasure(game_state):
    '''Функция проверяющая условия победы'''
    room_data =  ROOMS.get(game_state['current_room'])
    current_room = game_state['current_room']

    if 'treasure chest' in game_state['room_items'][current_room]:
        if 'treasure_key' in game_state['player_inventory']:
            print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
            game_state['room_items'][current_room].remove('treasure chest')
            print("В сундуке сокровище! Вы победили!")
            game_state['game_over'] = True
            return
        else:
            print("Ключа нет, но на сундуке есть код. Попробуешь решить? (да/нет)")
            answer = input('да/нет: ')
            if answer.lower() == 'да':
                code = input("Введите код: ")
                if code == room_data['puzzle'][1]:
                    print('Сокровище у Вас!')
                    game_state['room_items'][current_room].remove('treasure_chest')
                    game_state['game_over'] = True
                else:
                    print("Не подходит. Сундук все еще заперт")
            elif answer.lower() == 'нет':
                print("Вы отступаете от сундука.")
    
            
def show_help():
    '''Функция показа справки по командам'''
    from labyrinth_game.constants import COMMANDS
    
    print("\n=== ДОСТУПНЫЕ КОМАНДЫ ===")
    for command, description in COMMANDS.items():
        print(f"{command:<16} - {description}")
    print("========================\n")


def pseudo_random(seed, modulo):
    '''JФункция определения случайности в путешествии'''
    
    s_1 = seed * 28.333
    sin_seed = math.sin(s_1)
    s_2 = sin_seed * 6784.984
    s_3 = s_2 - math.floor(s_2)
    s_fin= s_3 * modulo
    return math.trunc(s_fin)

def trigger_trap(game_state):
    '''Функция создания ловушек.'''

    print("Ловушка активирована! Пол стал дрожать...")

    if game_state['player_inventory']:
        player_inv_len = len(game_state['player_inventory'])
        missing_index = pseudo_random(game_state['steps_taken'], player_inv_len)
        missing_item = game_state['player_inventory'][missing_index]
        game_state['player_inventory'].remove(missing_item)
        print('Неприятненько, но вы потеряли {missing_item}.')
    else:
        damage = pseudo_random(game_state['steps_taken'], MAX_DAMAGE)
        if damage < DAMAGE_THRESHOLD:
            print('Вы повержены.')
            game_state['game_over'] = True
        else:
            print('Вы ранены, но живы.')

def random_event(game_state):
    '''Функция создания случайных событий при перемещении'''

    check_event = pseudo_random(game_state['steps_taken'], EVENT_PROBABILITY)
    if check_event == 0:
        choose_event = pseudo_random(game_state['steps_taken'], EVENT_TYPES)
        has_torch = 'torch' in game_state['player_inventory']

        if choose_event == 0:
            print('Да вы счастливчик. Вы нашли монетку и положили ее в инвентарь')
            game_state['player_inventory'].append('coin')

        elif choose_event == 1:
            print('Во тьме слышится шорох')
            if 'sword' in game_state['player_inventory']:
                print('Вы достали меч и отпугнули существо.')
        
        elif choose_event == 2:
            if game_state['current_room'] == 'trap_room' and not has_torch:
                trigger_trap(game_state)
            

