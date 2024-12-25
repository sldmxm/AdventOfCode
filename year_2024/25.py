import time


def read_data(file_path: str) -> dict:
    with open(file_path) as f:
        blocks = f.read().split('\n\n')
    data = {'locks': [], 'keys': []}
    for block in blocks:
        lines = block.split('\n')
        data_type = 'locks' if set(lines[0]) == {'#'} else 'keys'
        data[data_type].append(lines)
    return data


def solve_part1(data):
    locks = []
    for lock in data['locks']:
        cur_lock = [col.count('#') - 1 for col in zip(*lock, strict=False)]
        locks.append(cur_lock)
    keys = []
    for key in data['keys']:
        cur_key = [col.count('#') - 1 for col in zip(*key, strict=False)]
        keys.append(cur_key)
    res = 0
    for lock in locks:
        for key in keys:
            overlaps = sum(1 for i in range(len(lock)) if lock[i] + key[i] > 5)
            res += overlaps == 0
    return res


def main():
    data = read_data('data/25.txt')

    start = time.monotonic()
    res = solve_part1(data)
    print('Part 1:', res)
    print(time.monotonic() - start)


if __name__ == '__main__':
    main()
