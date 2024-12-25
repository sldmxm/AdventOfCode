def read_data(
    file_path: str,
) -> dict[str, set[tuple[int, int]] | tuple | None]:
    data: dict[str, set[tuple[int, int]] | tuple | None] = {
        'obstructions': set(),
        'map_size': None,
        'start': None,
    }
    with open(file_path) as f:
        rows = f.readlines()
    for row_idx, row in enumerate(rows):
        for col_idx, char in enumerate(row):
            if char == '#':
                data['obstructions'].add((row_idx, col_idx))
            elif data['start'] is None and char in '^>v<':
                data['start'] = (row_idx, col_idx, char)
    data['map_size'] = (row_idx + 1, len(row.rstrip()))
    return data


def get_path(data: dict) -> list[tuple[int, int, str]] | None:
    DIRECTIONS = {
        '^': (-1, 0, '>'),
        '>': (0, 1, 'v'),
        'v': (1, 0, '<'),
        '<': (0, -1, '^'),
    }
    y, x, direction = data['start']
    n_rows, n_cols = data['map_size']
    obstructions = data['obstructions']
    path = []
    path_set = set()
    while True:
        if not (0 <= x < n_cols and 0 <= y < n_rows):
            return path
        if (y, x, direction) in path_set:
            return None
        path.append((y, x, direction))
        path_set.add((y, x, direction))

        dy, dx, next_direction = DIRECTIONS[direction]
        if (y + dy, x + dx) in obstructions:
            direction = next_direction
        else:
            x += dx
            y += dy


def count_distinct_positions(data: dict) -> int:
    path = get_path(data)
    if not path:
        return 0
    return len(set([(y, x) for y, x, _ in path]))


def count_new_obstructions(data: dict) -> int:
    path = get_path(data)
    if not path:
        return 0
    res = 0
    seen = {data['start'][:2]}
    for i, step in enumerate(path[1:]):
        if step[:2] not in seen:
            data['obstructions'].add(step[:2])
            data['start'] = path[i - 1]
            if not get_path(data):
                res += 1
            data['obstructions'].remove(step[:2])
        seen.add(step[:2])
    return res


def main():
    data = read_data('data/06_input.txt')
    print('Part 1:', count_distinct_positions(data))
    print('Part 2:', count_new_obstructions(data))


if __name__ == '__main__':
    main()
