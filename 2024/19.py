import time

def read_data(file_path: str) -> dict:
    with open(file_path) as f:
        towels, patterns = f.read().split('\n\n')
    data = {
        'towels': {item for item in towels.strip().split(', ')},
        'patterns': [item for item in patterns.split('\n')]
    }
    return data

def get_towels_trie(towels):
    root = {}
    for towel in towels:
        level = root
        for letter in towel:
            level[letter] = level.get(letter, {})
            level = level[letter]
        level[None] = towel
    return root

def solve_part1(data):
    def can_build_pattern(pattern):
        cache = {}
        def backtrack(idx):
            if idx in cache:
                return cache[idx]
            if idx == len(pattern):
                return True
            i = 0
            letter = pattern[idx]
            level = towels_trie
            while letter in level:
                level = level[letter]
                i += 1
                if None in level:
                    if backtrack(idx + i):
                        cache[idx] = True
                        return True
                if idx + i < len(pattern):
                    letter = pattern[idx + i]
                else:
                    break
            cache[idx] = False
            return False
        return backtrack(0)

    towels_trie = get_towels_trie(data['towels'])
    patterns = data['patterns']
    return sum(1 for pattern in patterns if can_build_pattern(pattern))

def solve_part2(data):
    def find_all_combinations(pattern):
        cache = {}
        def backtrack(idx):
            if idx in cache:
                return cache[idx]
            if idx == len(pattern):
                return 1

            level = towels_trie
            total_count = 0
            for i in range(idx, len(pattern)):
                letter = pattern[i]
                if letter not in level:
                    break
                level = level[letter]
                if None in level:
                    total_count += backtrack(i + 1)
            cache[idx] = total_count
            return total_count

        return backtrack(0)

    towels_trie = get_towels_trie(data['towels'])
    patterns = data['patterns']
    return sum(find_all_combinations(pattern) for pattern in patterns)


def main():
    start = time.monotonic()
    # data = read_data('data/test.txt')
    data = read_data('data/19.txt')
    res = solve_part1(data) # 260
    print('Part 1:', res)
    res = solve_part2(data) # 639963796864990
    print('Part 2:', res)
    print(time.monotonic() - start)


if __name__ == '__main__':
    main()
