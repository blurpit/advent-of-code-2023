def get_corresponding(mapping, src_num):
    for dst_start, src_start, length in mapping:
        if src_start <= src_num < src_start + length:
            return src_num - src_start + dst_start
    return src_num

def parse_mapping(string):
    lines = string.splitlines()
    mapping = []
    for line in lines[1:]:
        line = line.strip().split(' ')
        line = list(map(int, line))
        mapping.append(line)
    return mapping

def parse_seeds(string):
    seeds = string.removeprefix('seeds: ').split(' ')
    return list(map(int, seeds))

if __name__ == '__main__':
    with open('input.txt', 'r') as file:
        text = file.read().split('\n\n')

        seeds = text.pop(0)
        seeds = parse_seeds(seeds)

        mappings = [parse_mapping(string) for string in text]
        for mapping in mappings:
            for i, seed in enumerate(seeds):
                seeds[i] = get_corresponding(mapping, seed)
        print(min(seeds))
