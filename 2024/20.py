import collections
import time


def read_data(file_path: str) -> dict:
    with open(file_path) as f:
        lines = f.readlines()
    data = {
        'maze': [],
        'start': (0, 0),
        'end': (0, 0)
    }
    for row, line in enumerate(lines):
        line = line.strip()
        map_line = []
        for col, char in enumerate(line):
            if char == 'S':
                data['start'] = (row, col)
                char = '.'
            elif char == 'E':
                data['end'] = (row, col)
                char = '.'
            map_line.append(char)
        data['maze'].append(map_line)
    return data


def get_best_path(data):
    MOVES = ((0, 1), (1, 0), (0, -1), (-1, 0))
    end, maze = data['end'], data['maze']
    y, x = data['start']
    path, step = [(y, x)], 0
    queue = collections.deque([(y, x, path)])
    seen = {(y, x): step}
    best_path = {}
    while queue:
        y, x, path = queue.popleft()
        step = len(path)
        if (y, x) == end:
            for i in range(len(path)):
                y, x = path[i]
                best_path[(y, x)] = i
        if end in seen and step >= seen[end]:
            return best_path
        for dy, dx in MOVES:
            ny, nx = y + dy, x + dx
            if maze[ny][nx] == '.':
                if (ny, nx) not in seen or seen[(ny, nx)] >= step + 1:
                    new_path = path + [(ny, nx)]
                    queue.append((ny, nx, new_path))
                    seen[(ny, nx)] = step + 1


def solve_part1(data, min_cheat_result=0):
    DIRECTIONS = ((0, 1), (1, 0), (0, -1), (-1, 0))
    best_path = get_best_path(data)
    maze = data['maze']
    cheats = set()
    for (y, x), step in best_path.items():
        for dy, dx in DIRECTIONS:
            ny, nx = y + dy, x + dx
            if (
                    (ny + dy, nx + dx) in best_path
                    and maze[ny][nx] == '#'
                    and best_path[(ny + dy, nx + dx)] > step + 2
            ):
                cheat_result = best_path[(ny + dy, nx + dx)] - (step + 2)
                cheats.add(((ny, nx), (ny + dy, nx + dx), cheat_result))
    cheat_counter = sum(
        1 for _, _, result in cheats if result >= min_cheat_result)
    return cheat_counter


def solve_part2(data, min_cheat_result=0):
    best_path = get_best_path(data)
    path = [0] * len(best_path)
    for (y, x), step in best_path.items():
        path[step] = (y, x)
    cheats = {}
    for start_step in range(len(path) - min_cheat_result):
        sy, sx = path[start_step]
        for end_step in range(
                start_step + min_cheat_result, len(path)):
            ey, ex = path[end_step]
            if abs(ey - sy) + abs(ex - sx) <= 20:
                result = (end_step - start_step) - (abs(ey - sy) + abs(ex - sx))
                cheats[((sy, sx), (ey, ex))] = result
    cheat_counter = sum(
        1 for result in cheats.values() if result >= min_cheat_result)
    return cheat_counter


def solve_part2_bfs(data, min_cheat_result=0):
    MOVES = ((0, 1), (1, 0), (0, -1), (-1, 0))
    maze = data['maze']
    best_path = get_best_path(data)
    cheats = {}
    for (sy, sx), start_step in best_path.items():
        if len(best_path) - start_step > min_cheat_result:
            step = 0
            queue = collections.deque([(sy, sx, step)])
            seen = {(sy, sx), }
            while queue:
                y, x, step = queue.popleft()
                if (y, x) in best_path:
                    result = best_path[(y, x)] - start_step - step
                    if result >= min_cheat_result:
                        cheats[((sy, sx), (y, x))] = result
                for dy, dx in MOVES:
                    ny, nx = y + dy, x + dx
                    if (
                            0 < ny < len(maze) - 1
                            and 0 < nx < len(maze[0]) - 1
                            and step < 20
                            and (ny, nx) not in seen
                    ):
                        queue.append((ny, nx, step + 1))
                        seen.add((ny, nx))
    cheat_counter = sum(
        1 for result in cheats.values() if result >= min_cheat_result)
    return cheat_counter


def main():
    data = read_data('data/20.txt')

    start = time.monotonic()
    res = solve_part1(data, 100)
    print('Part 1:', res)  # 1293
    print(time.monotonic() - start)

    start = time.monotonic()
    res = solve_part2(data, 100)
    print('Part 2:', res)  # 977747
    print(time.monotonic() - start)

    start = time.monotonic()
    res = solve_part2_bfs(data, 100)
    print('Part 2:', res)  # 977747
    print(time.monotonic() - start)


if __name__ == '__main__':
    main()
