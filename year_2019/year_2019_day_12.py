import math
import time

from utils.download_data import download_data


def read_data(file_path: str) -> list[list[int]]:
    with open(file_path) as f:
        lines = f.readlines()
    data = []
    for line in lines:
        data.append(
            [
                int(item.split('=')[1])
                for item in line.strip()[1:-1].split(', ')
            ]
        )
    return data


def next_move_inplace(pos: list[list[int]], vel: list[list[int]]) -> None:
    for moon in range(len(pos)):
        for other_moon in range(moon, len(pos)):
            for i in range(3):
                if pos[moon][i] < pos[other_moon][i]:
                    vel[moon][i] += 1
                    vel[other_moon][i] -= 1
                elif pos[moon][i] > pos[other_moon][i]:
                    vel[moon][i] -= 1
                    vel[other_moon][i] += 1
        pos[moon] = [pos[moon][i] + vel[moon][i] for i in range(3)]


def solve_part1(data: list[list[int]], steps: int) -> int:
    pos = data[:]
    vel = [[0] * len(pos[0]) for _ in range(len(pos))]
    for _ in range(steps):
        next_move_inplace(pos, vel)

    total = 0
    for moon in range(len(pos)):
        pot = sum(abs(c) for c in pos[moon])
        kin = sum(abs(v) for v in vel[moon])
        total += pot * kin
    return total


def solve_part2(data: list[list[int]]) -> int:
    pos = data[:]
    vel = [[0] * len(pos[0]) for _ in range(len(pos))]
    step = 0
    initial_state = [
        (
            tuple(pos[moon][i] for moon in range(len(pos))),
            tuple(vel[moon][i] for moon in range(len(vel))),
        )
        for i in range(3)
    ]
    seen = [[0] for _ in range(3)]
    while True:
        next_move_inplace(pos, vel)
        step += 1
        cur = [
            (
                tuple(pos[moon][i] for moon in range(len(pos))),
                tuple(vel[moon][i] for moon in range(len(vel))),
            )
            for i in range(3)
        ]
        for i in range(3):
            if cur[i] == initial_state[i]:
                seen[i].append(step)

        if all(len(seen[i]) >= 2 for i in range(3)):
            break

    tx, ty, tz = [seen[i][-1] for i in range(3)]
    res = tx * ty // math.gcd(tx, ty)
    res = tz * res // math.gcd(res, tz)
    return res


def main() -> None:
    data_file_path = None
    try:
        data_file_path = download_data(__file__)
    except Exception as e:
        print(f'ERROR: {e}')

    if data_file_path:
        data = read_data(data_file_path)

        start = time.monotonic()
        res1 = solve_part1(data, 1000)
        print('Part 1:', res1)
        print(time.monotonic() - start)

        start = time.monotonic()
        res2 = solve_part2(data)
        print('Part 2:', res2)
        print(time.monotonic() - start)


if __name__ == '__main__':
    main()
