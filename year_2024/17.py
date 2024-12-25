import collections
import time


def read_data(file_path: str) -> list:
    with open(file_path) as f:
        lines = f.readlines()
    data = []
    for line in lines:
        line = line.strip()
        if line.startswith('Register'):
            parts = line.split(': ')
            data.append(int(parts[1]))
        elif line.startswith('Program'):
            parts = line.split(': ')
            data.append([int(n) for n in parts[1].split(',')])
    return data


def compute(data):
    a, b, c, program = data
    registers = [a, b, c]
    res = []
    i = 0
    while i < len(program):
        command, l_operand = program[i : i + 2]
        c_operand = (
            registers[l_operand - 4] if 3 < l_operand < 7 else l_operand
        )
        match command:
            case 0:
                registers[0] >>= c_operand
            case 1:
                registers[1] ^= l_operand
            case 2:
                registers[1] = c_operand & 7
            case 3:
                if registers[0] != 0:
                    i = l_operand
                    continue
            case 4:
                registers[1] ^= registers[2]
            case 5:
                res.append(c_operand & 7)
            case 6:
                registers[1] = registers[0] >> c_operand
            case 7:
                registers[2] = registers[0] >> c_operand
        i += 2
    return res


def solve_part1(data):
    return ','.join([str(n) for n in compute(data)])


def solve_part2(data):
    program = data[-1]
    queue = collections.deque([(1, 0)])
    while queue:
        step, start = queue.popleft()
        for a in range(start, start + 8):
            data[0] = a
            cur = compute(data)
            if cur == program:
                return a
            elif cur == program[-step:]:
                queue.append((step + 1, a << 3))


def main():
    start = time.monotonic()
    data = read_data('data/17.txt')
    res = solve_part1(data)
    print('Part 1:', res)
    res = solve_part2(data)
    print('Part 2:', res)
    print(time.monotonic() - start)


if __name__ == '__main__':
    main()
