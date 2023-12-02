def parse_game(line):
    game_id, _, game = line.partition(': ')
    game_id = int(game_id.removeprefix('Game '))

    game = game.strip().split('; ')
    game = [
        dict(
            parse_cubes(cubes)
            for cubes in handfull.split(', ')
        )
        for handfull in game
    ]
    return game_id, game

def parse_cubes(cubes):
    """ "8 green" -> ('green', 8) """
    cubes = cubes.split(' ', 1)
    return cubes[1], int(cubes[0])

def smallest_bag(game):
    bag = {}
    for handfull in game:
        for color, count in handfull.items():
            bag[color] = max(count, bag.get(color, 0))
    return bag

def power(bag):
    return bag['red'] * bag['green'] * bag['blue']

if __name__ == '__main__':
    answer = 0
    with open('input.txt', 'r') as file:
        for line in file.readlines():
            game_id, game = parse_game(line)
            answer += power(smallest_bag(game))
    print(answer)
