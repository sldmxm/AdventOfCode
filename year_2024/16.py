import heapq
import time


def read_data(file_path: str) -> dict:
    with open(file_path) as f:
        lines = f.readlines()
    data = {'maze': [], 'start': (0, 0), 'end': (0, 0)}
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


def solve_part1(data):
    MOVES = (
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0),
    )
    end, maze = data['end'], data['maze']
    y, x = data['start']
    score, direction = 0, 0
    heap = [(score, y, x, direction)]
    seen = {
        (y, x),
    }
    while heap:
        score, y, x, direction = heapq.heappop(heap)
        if (y, x) == end:
            return score
        for new_direction, (dy, dx) in enumerate(MOVES):
            ny, nx = y + dy, x + dx
            if (maze[ny][nx] == '.' and (ny, nx) not in seen) or (
                ny,
                nx,
            ) == end:
                rotate = abs(new_direction - direction)
                add_score = 1 + 1000 * (rotate if not rotate % 2 else 1)
                heapq.heappush(
                    heap, (score + add_score, ny, nx, new_direction)
                )
                seen.add((ny, nx))


def solve_part2(data):
    MOVES = (
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0),
    )
    end, maze = data['end'], data['maze']
    y, x = data['start']
    path = [(y, x)]
    score, direction = 0, 0
    heap = [(score, y, x, direction, path)]
    seen = {(y, x): score}
    best_paths = set()
    while heap:
        score, y, x, direction, path = heapq.heappop(heap)
        if (y, x) == end:
            best_paths |= set(path)
        if end in seen and score >= seen[end]:
            return len(best_paths)
        for new_direction, (dy, dx) in enumerate(MOVES):
            ny, nx = y + dy, x + dx
            if maze[ny][nx] == '.':
                rotate = abs(new_direction - direction)
                new_score = (
                    score + 1 + 1000 * (rotate if not rotate % 2 else 1)
                )
                if (ny, nx) not in seen or seen[(ny, nx)] >= new_score - 1001:
                    new_path = path + [(ny, nx)]
                    heapq.heappush(
                        heap, (new_score, ny, nx, new_direction, new_path)
                    )
                    seen[(ny, nx)] = new_score


def main():
    start = time.monotonic()
    # data = read_data('test.txt')
    data = read_data('data/16.txt')
    res = solve_part1(data)
    print('Part 1:', res)  # 109516
    res = solve_part2(data)  # 568
    print('Part 2:', res)
    print(time.monotonic() - start)


if __name__ == '__main__':
    main()
