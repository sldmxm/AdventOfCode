import collections
import heapq
import time

def read_data(file_path: str) -> list:
    with open(file_path) as f:
        lines = f.readlines()
    data = []
    for line in lines:
        data.append(tuple(map(int, line.strip().split(','))))
    return data

def solve_part1(data, maze_size, byte_size):
    MOVES = ((0, 1), (1, 0), (0, -1), (-1, 0),)
    corrupted = set(data[:byte_size])
    x, step, y = 0, 0, 0
    seen = {(y, x)}
    queue = collections.deque([(y, x, step)])
    while queue:
        y, x, step = queue.popleft()
        if (y, x) == (maze_size - 1, maze_size - 1):
            return step
        for dy, dx in MOVES:
            ny, nx = y + dy, x + dx
            if (
                    0 <= ny < maze_size
                    and 0 <= nx < maze_size
                    and (nx, ny) not in corrupted
                    and (ny, nx) not in seen
            ):
                queue.append((ny, nx, step + 1))
                seen.add((ny, nx))

def solve_part2(data, maze_size, byte_size):
    l, r =  byte_size, len(data)
    while l < r - 1:
        mid = (l + r) // 2
        if solve_part1(data, maze_size, mid):
            l = mid
        else:
            r = mid - 1
    return data[r]

def main():
    start = time.monotonic()
    # data = read_data('test.txt')
    # res = solve_part1(data, 7, 12)
    data = read_data('data/18.txt')
    res = solve_part1(data, 71, 1024)
    print('Part 1:', res)
    res = solve_part2(data, 71, 1024)
    print('Part 2:', res)
    print(time.monotonic() - start)


if __name__ == '__main__':
    main()
