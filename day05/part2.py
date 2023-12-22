def range_overlap(src_start, dst_start, length, seed_start, seed_end):
    """ returns a list of ranges """
    result = []
    src_end = src_start + length

    # seed & src do not overlap at all
    if src_end <= seed_start:
        return result

    # add seed before src starts
    if src_start > seed_start:
        result.append((seed_start, src_start))

    # add src & seed overlap range, convert to dst
    result.append((
        max(seed_start, src_start) - src_start + dst_start,
        min(seed_end, src_end) - src_start + dst_start
    ))

    return result

def get_corresponding_ranges(mapping, seed_start, seed_end):
    result = []
    for dst_start, src_start, length in mapping:
        if seed_start >= seed_end:
            # no more seed left
            break
        src_end = src_start + length
        result.extend(range_overlap(
            src_start, dst_start, length,
            seed_start, seed_end
        ))
        # update seed start to remove the part that has been added
        seed_start = max(seed_start, src_end)

    # Add excess
    if seed_start < seed_end:
        result.append((seed_start, seed_end))

    return result

def parse_mapping(string):
    lines = string.splitlines()
    mapping = []
    for line in lines[1:]:
        line = line.strip().split(' ')
        line = tuple(map(int, line))
        mapping.append(line)
    # sort mapping by source start
    mapping.sort(key=lambda x: x[1])
    return mapping

def parse_seeds(string):
    seeds = string.removeprefix('seeds: ').split(' ')
    result = []
    for i in range(len(seeds) // 2):
        seed_start = int(seeds[2*i])
        seed_end = int(seeds[2*i+1]) + seed_start
        result.append((seed_start, seed_end))
    return result

if __name__ == '__main__':
    with open('input.txt', 'r') as file:
        text = file.read().split('\n\n')

        seeds = text.pop(0)
        seeds = parse_seeds(seeds)

        mappings = [parse_mapping(string) for string in text]
        for mapping in mappings:
            next_seeds = []
            for seed_start, seed_end in seeds:
                next_seeds.extend(get_corresponding_ranges(mapping, seed_start, seed_end))
            seeds = next_seeds

        answer = float('inf')
        for start, _ in seeds:
            answer = min(answer, start)
        print(answer)
