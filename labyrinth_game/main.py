#!/usr/bin/env python3
from labyrinth_game.constants import ROOMS
from labyrinth_game.player_actions import (
    get_input,
    move_player,
    show_inventory,
    take_item,
    use_item,
)
from labyrinth_game.utils import (
    attempt_open_treasure,
    describe_current_room,
    show_help,
    solve_puzzle,
)

game_state = {
        'player_inventory': [], # Инвентарь игрока
        'current_room': 'entrance', # Текущая комната
        'game_over': False, # Значения окончания игры
        'steps_taken': 0, # Количество шагов
        'room_items': {} , # текущие предметы в комнатах
        'solved_puzzles': [], # решенные загадки
        'reward': 0 #количество наград
    }

def process_command(game_state, command):
    '''Обработка команд'''
    from labyrinth_game.constants import DIRECTIONS

    parts = command.split()
    action = parts[0] if parts else ""
    argument = ' '.join(parts[1:]) if len(parts) > 1 else ""

    match action:
        case direction if direction in DIRECTIONS:
            move_player(game_state, direction)
        case 'look':
            describe_current_room(game_state)
        case 'use':
            if argument == 'treasure_chest':
                attempt_open_treasure(game_state)
            else:
                use_item(game_state, argument)
        case 'go':
            move_player(game_state, argument)
        case 'take':
            take_item(game_state, argument)
        case 'inventory':
            show_inventory(game_state)
        case 'quit':
            game_state['game_over'] = True
        case 'exit':
            game_state['game_over'] = True
        case 'solve':
            if game_state['current_room'] == 'treasure_room':
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)
        case 'help':
            show_help()
        case _:
            print("Неизвестная команда.")

def main():
    """Основная функция программы"""
    print("Добро пожаловать в Лабиринт сокровищ!")

        # Инициализация предметов комнат (копируем из ROOMS)
    for room_name, room_data in ROOMS.items():
        game_state['room_items'][room_name] = room_data['items'].copy()

    describe_current_room(game_state)
    
    while not game_state['game_over']:
        command =  command = get_input("\nЧто дальше: ")
        process_command(game_state, command)

         

if __name__ == "__main__":
    # Этот код выполнится только при прямом запуске модуля
    main()