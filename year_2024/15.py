import time
from copy import deepcopy


def read_data(file_path: str) -> dict:
    with open(file_path) as f:
        lines = f.readlines()
    data = {'map': [], 'code': [], 'start': (0, 0)}
    block = 'map'
    for row, line in enumerate(lines):
        line = line.strip()
        if line == '':
            block = 'code'
        if block == 'map':
            map_line = []
            for col, char in enumerate(line):
                if char == '@':
                    data['start'] = (row, col)
                    char = '.'
                map_line.append(char)
            line = map_line
        data[block].append(line)
    data['code'] = ''.join(data['code'])
    return data


def solve_part1(data):
    COMMANDS = {
        '<': (0, -1),
        '^': (-1, 0),
        '>': (0, 1),
        'v': (1, 0),
    }
    (y, x), map, code = data['start'], deepcopy(data['map']), data['code']
    for command in code:
        dy, dx = COMMANDS[command]
        ny, nx = y + dy, x + dx
        if map[ny][nx] == 'O':
            layer, next_cell = 0, ''
            while next_cell not in {'.', '#'}:
                layer += 1
                next_cell = map[ny + layer * dy][nx + layer * dx]
            if next_cell == '.':
                map[ny + layer * dy][nx + layer * dx] = 'O'
                map[ny][nx] = '.'
                y, x = ny, nx
        elif map[ny][nx] == '.':
            y, x = ny, nx
    res = 0
    for y in range(len(map)):
        for x in range(len(map[0])):
            if map[y][x] == 'O':
                res += y * 100 + x
    return res


def solve_part2(data):
    COMMANDS = {
        '<': (0, -1),
        '^': (-1, 0),
        '>': (0, 1),
        'v': (1, 0),
    }
    (y, x), code = data['start'], data['code']
    x *= 2
    map = []
    for row in data['map']:
        map_line = []
        for char in row:
            if char == 'O':
                map_line.extend(['[', ']'])
            else:
                map_line.extend([char] * 2)
        map.append(map_line)

    for command in code:
        dy, dx = COMMANDS[command]
        ny, nx = y + dy, x + dx
        if map[ny][nx] in {'[', ']'}:
            if dx:
                layer, next_cell = 0, ''
                while next_cell not in {'.', '#'}:
                    layer += 1
                    next_cell = map[ny][nx + layer * dx]
                if next_cell == '.':
                    char = '[' if dx == 1 else ']'
                    for i in range(1, layer + 1):
                        map[ny][nx + i * dx] = char
                        char = '[' if char == ']' else ']'
                    map[ny][nx] = '.'
                    y, x = ny, nx
            else:
                left_x, right_x = (
                    (nx, nx + 1) if map[ny][nx] == '[' else (nx - 1, nx)
                )
                stack = [
                    [(ny, left_x, right_x)],
                ]
                layer = 0
                while True:
                    layer += 1
                    next_layer_y = ny + layer * dy
                    cur_layer = []
                    next_layer_chars = set()
                    for _, left_x, right_x in stack[-1]:
                        next_layer_chars |= set(
                            map[next_layer_y][left_x : right_x + 1]
                        )
                    if next_layer_chars == {'.'} or '#' in next_layer_chars:
                        break
                    for _, left_x, right_x in stack[-1]:
                        match map[next_layer_y][left_x]:
                            case ']':
                                cur_layer.append(
                                    (next_layer_y, left_x - 1, left_x)
                                )
                            case '[':
                                cur_layer.append(
                                    (next_layer_y, left_x, right_x)
                                )
                        if map[next_layer_y][right_x] == '[':
                            cur_layer.append(
                                (next_layer_y, right_x, right_x + 1)
                            )
                    stack.append(cur_layer)
                if next_layer_chars == {'.'}:
                    while stack:
                        layer = stack.pop()
                        for box in layer:
                            box_y, left_x, right_x = box
                            (
                                map[box_y + dy][left_x],
                                map[box_y + dy][right_x],
                            ) = '[', ']'
                            map[box_y][left_x], map[box_y][right_x] = '.', '.'
                    y, x = ny, nx

        elif map[ny][nx] == '.':
            y, x = ny, nx
        #
        # tmp = deepcopy(map)
        # tmp[y][x] = command
        # print(y, x, ny, nx, map[ny][ny])
        # print(*[''.join(row) for row in tmp], sep='\n')

    res = 0
    for y in range(len(map)):
        for x in range(len(map[0])):
            if map[y][x] == '[':
                res += y * 100 + x
    return res


def main():
    start = time.monotonic()
    data = read_data('data/15.txt')
    res = solve_part1(data)
    print('Part 1:', res)
    res = solve_part2(data)
    print('Part 2:', res)
    print(time.monotonic() - start)


if __name__ == '__main__':
    main()
