import time


def read_data(file_path: str) -> dict:
    data = {
        'antennas': {},
        'map_size': None,
    }
    with open(file_path) as f:
        rows = f.readlines()
    for row_idx, row in enumerate(rows):
        for col_idx, char in enumerate(row.rstrip()):
            if char != '.':
                data['antennas'][char] = data['antennas'].get(char, []) + [
                    (row_idx, col_idx)
                ]
    data['map_size'] = (row_idx + 1, len(row))
    return data


def count_antinodes_part1(data) -> int:
    antinodes = set()
    antennas = data['antennas']
    n_rows, n_cols = data['map_size']
    for antenna_type in antennas:
        for i, first_antenna in enumerate(antennas[antenna_type][:-1]):
            f_y, f_x = first_antenna
            for second_antenna in antennas[antenna_type][i + 1 :]:
                s_y, s_x = second_antenna
                dy, dx = (s_y - f_y, s_x - f_x)
                antinodes |= {
                    (y, x)
                    for y, x in ((f_y - dy, f_x - dx), (s_y + dy, s_x + dx))
                    if 0 <= x < n_cols and 0 <= y < n_rows
                }
    return len(antinodes)


def count_antinodes_part2(data) -> int:
    antinodes = set()
    antennas = data['antennas']
    n_rows, n_cols = data['map_size']
    for antenna_type in antennas:
        for i, first_antenna in enumerate(antennas[antenna_type][:-1]):
            f_y, f_x = first_antenna
            for second_antenna in antennas[antenna_type][i + 1 :]:
                s_y, s_x = second_antenna
                dy, dx = (s_y - f_y, s_x - f_x)
                y, x = f_y, f_x
                while 0 <= x < n_cols and 0 <= y < n_rows:
                    antinodes |= {(y, x)}
                    y += dy
                    x += dx
                y, x = f_y, f_x
                while 0 <= x < n_cols and 0 <= y < n_rows:
                    antinodes |= {(y, x)}
                    y -= dy
                    x -= dx
    return len(antinodes)


def main():
    data = read_data('data/08_input.txt')
    start = time.monotonic()
    res1 = count_antinodes_part1(data)
    res2 = count_antinodes_part2(data)
    print('Part 1:', res1)
    print('Part 2:', res2)
    print(time.monotonic() - start)


if __name__ == '__main__':
    main()
