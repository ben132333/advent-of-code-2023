import re

bag_dice_count = {
    'red': 12,
    'green': 13,
    'blue': 14
}

def process_input(input_document):
    input_games = []
    for game in input_document:
        new_game = {}
        
        game = game.strip()
        game_id, game_sets = game.split(':')
        
        # Get the id
        id = re.search(r'\d+', game_id)
        new_game['id'] = int(id.group(0))

        # Get the game sets
        new_game['sets'] = []

        game_sets = game_sets.split(';')
        for set in game_sets:
            new_set = {}

            set = set.strip()
            set = set.split(',')
            for dice in set:
                if 'red' in dice:
                    new_set['red'] = int(re.search(r'\d+', dice).group(0))
                elif 'green' in dice:
                    new_set['green'] = int(re.search(r'\d+', dice).group(0))
                elif 'blue' in dice:
                    new_set['blue'] = int(re.search(r'\d+', dice).group(0))

            new_game['sets'].append(new_set)                 
        
        input_games.append(new_game)
    
    return input_games

def is_set_valid(set):
    for color in ['red', 'green', 'blue']:
        if color in set:
            if set[color] > bag_dice_count[color]:
                return False
    
    return True

def is_game_valid(game):
    for set in game['sets']:
        if not is_set_valid(set):
            return False
    
    return True

def get_fewest_dice_set(game):
    fewest_dice = {'red': 0, 'green': 0, 'blue': 0}

    for set in game['sets']:
        for color in ['red', 'green', 'blue']:
            if color in set:
                fewest_dice[color] = max(fewest_dice[color], set[color])
    
    return fewest_dice

def power_of_set(set):
    power = 1
    for color in ['red', 'green', 'blue']:
        if color in set:
            power *= set[color]
    
    return power

if __name__ == "__main__":
    with open('aoc_day2_input.txt') as f:
        input_document = f.readlines()
    input_games = process_input(input_document)
    
    # Part 1
    result = 0
    for game in input_games:
        result += game['id']
    print(result)

    # Part 2
    power_sum = 0
    for game in input_games:
        fewest_dice = get_fewest_dice_set(game)
        power_sum += power_of_set(fewest_dice)
    print(power_sum)

