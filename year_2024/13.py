import time
from dataclasses import dataclass


@dataclass
class Machine:
    ax: int
    ay: int
    bx: int
    by: int
    goal_x: int
    goal_y: int


def read_data(file_path: str) -> list[Machine]:
    with open(file_path) as f:
        lines = f.readlines()
    data = []
    cur_data = []
    for line in lines:
        line = line.strip()
        if line.startswith('Button A') or line.startswith('Button B'):
            parts = line.split(', ')
            x_part = parts[0].split('+')
            y_part = parts[1].split('+')
            cur_data.extend([int(x_part[1]), int(y_part[1])])
        elif line.startswith('Prize'):
            parts = line.split(', ')
            x_part = parts[0].split('=')
            y_part = parts[1].split('=')
            cur_data.extend([int(x_part[1]), int(y_part[1])])
            data.append(Machine(*cur_data))
            cur_data = []
    return data


def solve(machines, is_part1):
    res = 0
    for m in machines:
        if not is_part1:
            m.goal_x += 10_000_000_000_000
            m.goal_y += 10_000_000_000_000
        cost = 0
        det = m.ax * m.by - m.bx * m.ay
        if (m.goal_x * m.by - m.goal_y * m.bx) % det == 0 and (
            m.ax * m.goal_y - m.ay * m.goal_x
        ) % det == 0:
            a_count = (m.goal_x * m.by - m.goal_y * m.bx) // det
            b_count = (m.ax * m.goal_y - m.ay * m.goal_x) // det
            cost = a_count * 3 + b_count
            if is_part1 and (a_count > 100 or b_count > 100):
                cost = 0
        res += cost
    return res


def main():
    data = read_data('data/13.txt')
    start = time.monotonic()
    res = solve(data, is_part1=True)
    print('Part 1:', res)  # 30413
    res = solve(data, is_part1=False)
    print('Part 2:', res)  # 92827349540204
    print(time.monotonic() - start)


if __name__ == '__main__':
    main()
