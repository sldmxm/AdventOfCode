import time

CODE_KEYS = {char: (i // 3, i % 3) for i, char in enumerate('789456123 0A')}
DIRECTION_KEYS = {char: (i // 3, i % 3) for i, char in enumerate(' ^A<v>')}


def read_data(file_path: str) -> list:
    with open(file_path) as f:
        data = f.read().split('\n')
    return data


class Keypad:
    def __init__(self, keys: dict):
        self.keys = keys
        self.y, self.x = self.keys['A']
        self.coordinates = {(y, x): c for c, (y, x) in keys.items()}

    def move(self, direction: str):
        DIRECTIONS = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}
        dy, dx = DIRECTIONS[direction]
        self.y += dy
        self.x += dx

    def go_to_key(self, key: str) -> str:
        DIRECTIONS = {
            '^': (-1, 0),
            '>': (0, 1),
            'v': (1, 0),
            '<': (0, -1),
        }
        ny, nx = self.keys[key]
        is_empty_cell_on_path_y = (self.y, 0) == self.keys[' '] and nx == 0
        is_empty_cell_on_path_x = self.x == 0 and ny == self.keys[' '][0]
        PRIORITY = {
            '^': -1 * (10 if is_empty_cell_on_path_y else 1),
            '>': -1 * (10 if is_empty_cell_on_path_x else 1),
            'v': -2 * (10 if is_empty_cell_on_path_y else 1),
            '<': -3 * (10 if is_empty_cell_on_path_x else 1),
        }
        directions = set()
        if ny > self.y:
            directions.add('v')
        elif ny < self.y:
            directions.add('^')
        if nx > self.x:
            directions.add('>')
        elif nx < self.x:
            directions.add('<')
        path = []
        while self.y != ny or self.x != nx:
            if self.y == ny:
                directions &= {'>', '<'}
            if self.x == nx:
                directions &= {'^', 'v'}
            for direction in directions:
                dy, dx = DIRECTIONS[direction]
                if (self.y + dy, self.x + dx) != self.keys[' ']:
                    path.append(direction)
                    self.y += dy
                    self.x += dx
        path.sort(key=lambda char: (PRIORITY[char], char))
        path.append('A')
        return ''.join(path)

    def key(self) -> str:
        return self.coordinates[(self.y, self.x)]


def get_prev(data, keypad):
    test_robot = Keypad(keypad)
    prev = []
    for command in data:
        if command == 'A':
            prev.append(test_robot.key())
        else:
            test_robot.move(command)
    return ''.join(prev)


def solve(data, robots_count):
    res = 0
    for code in data:
        code_keypad = Keypad(CODE_KEYS)
        code_layer = []
        for char in code:
            code_layer.append(code_keypad.go_to_key(char))
        code_layer = ''.join(code_layer)
        for _ in range(robots_count - 1):
            robot_keypad = Keypad(DIRECTION_KEYS)
            next_layer_code = []
            for command in code_layer:
                next_layer_code.append(robot_keypad.go_to_key(command))
            code_layer = ''.join(next_layer_code)
        res += len(code_layer) * int(code[:-1])
    return res


def solve_fast(data, robots_count):
    def get_code_counter(keypad, pre_code, count):
        y, x = keypad['A']
        empty_y, empty_x = keypad[' ']
        path_counter = {}
        for char in pre_code:
            ny, nx = keypad[char]
            is_empty_cell_on_path = (
                y == empty_y
                and nx == empty_x
                or x == empty_x
                and ny == empty_y
            )
            move = (ny - y, nx - x, is_empty_cell_on_path)
            path_counter[move] = path_counter.get(move, 0) + count
            y, x = ny, nx
        return path_counter

    res = 0
    for code in data:
        code_layer_counter = get_code_counter(CODE_KEYS, code, 1)
        for _ in range(robots_count + 1):
            next_code_layer_counter = {}
            for (
                y,
                x,
                is_empty_cell_on_path,
            ), count in code_layer_counter.items():
                # moves = ''
                # moves += (-x * '<') if x < 0 else ''
                # moves += (y * 'v') if y > 0 else ''
                # moves += (-y * '^') if y < 0 else ''
                # moves += (x * '>') if x > 0 else ''
                # if is_empty_cell_on_path:
                #     moves = moves[::-1]
                # moves += 'A'

                # так проще, конечно,
                # - отрицательные значения просто не добавятся в строку
                moves = ('<' * -x + 'v' * y + '^' * -y + '>' * x)[
                    :: -1 if is_empty_cell_on_path else 1
                ] + 'A'
                step_code_counter = get_code_counter(
                    DIRECTION_KEYS, moves, count
                )
                for key, count in step_code_counter.items():
                    next_code_layer_counter[key] = (
                        next_code_layer_counter.get(key, 0) + count
                    )
            code_layer_counter = next_code_layer_counter

        res += sum(code_layer_counter.values()) * int(code[:-1])
    return res


def main():
    # data = read_data('data/test.txt')
    data = read_data('data/21.txt')

    start = time.monotonic()
    res = solve(data, 3)
    print('Part 1:', res)  # 176650
    print(time.monotonic() - start)

    start = time.monotonic()
    res = solve_fast(data, 2)
    print('Part 1:', res)
    res = solve_fast(data, 25)
    print('Part 2:', res)  # 217698355426872
    print(time.monotonic() - start)


if __name__ == '__main__':
    main()
