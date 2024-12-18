import time

def read_data(file_path: str) -> list[str]:
    with open(file_path) as f:
        rows = f.readlines()
    data = [row.rstrip() for row in rows]
    return data

def get_path_sides(y_start, x_start, shape):
    # finds only outer sides (
    y, x = y_start, x_start
    sides = 1
    directions = ((0, 1), (1, 0), (0, -1), (-1, 0))
    direction = 0
    while True:
        left_hand = (direction + 3) % 4
        dy, dx = directions[left_hand]
        ny, nx = y + dy, x + dx
        if (ny, nx) in shape:
            y, x = ny, nx
            sides += 1
            direction = left_hand
        else:
            for _ in range(3):
                dy, dx = directions[direction]
                ny, nx = y + dy, x + dx
                if (ny, nx) in shape:
                    y, x = ny, nx
                    break
                else:
                    direction = (direction + 1) % 4
                    sides += 1
        if (y, x) == (y_start, x_start):
            i = 0
            while direction != 0:
                i += 1
                direction = (direction + 1) % 4
            sides += i - 1
            break
    return sides

def get_sides_by_corners(shape):
    # doesn't work properly on the full dataset (
    CORNERS = ((-1, -1), (-1, 1), (1, 1), (1, -1),)
    NEIGHBORS_COUNTERCLOCKWISE = ((1, 0), (0, 1), (-1, 0), (0, -1), (1, 0),)
    sides = 0
    for y, x in shape:
        corners_to_check = {
            (dy, dx) for dy, dx in CORNERS
            if (y + dy, x + dx) not in shape
        }
        corners = []
        for corner_dy, corner_dx in corners_to_check:
            if (
                    (corner_dy + y, x) not in shape and (y, corner_dx + x) not in shape
                    or (corner_dy + y, x) in shape and (y, corner_dx + x) in shape
            ):
                corners.append((corner_dy, corner_dx))
        sides += len(corners)

        if not len(corners):
            count = 0
            for dy, dx in NEIGHBORS_COUNTERCLOCKWISE:
                if (y + dy, x + dx) not in shape:
                    if count:
                        sides += 1
                        break
                    else:
                        count += 1
                else:
                    count = 0
    return sides

def get_sides_scan(shape):
    PATTERNS = (
        ((-1, 0), (0, -1), (-1, -1)),  # upper side
        ((0, -1), (-1, 0), (-1, -1)),  # left side
        ((1, 0), (0, -1), (1, -1)),  # bottom side
        ((0, 1), (-1, 0), (-1, 1)),  # right side
    )

    first_row = min(y for y, _ in shape)
    first_col = min(x for _, x in shape)
    last_row = max(y for y, _ in shape)
    last_col = max(x for _, x in shape)
    sides = 0
    for y in range(first_row, last_row + 1):
        for x in range(first_col, last_col + 1):
            if (y, x) in shape:
                for trigger, not_in_shape, in_shape in PATTERNS:
                    if (
                            (y + trigger[0], x + trigger[1]) not in shape
                            and (
                            (y + not_in_shape[0], x + not_in_shape[1]) not in shape
                            or (y + in_shape[0], x + in_shape[1]) in shape
                    )
                    ):
                        sides += 1
    return sides

def solve(data) -> (int, int):
    res_part1 = 0
    res_part2 = 0
    seen = set()
    for row in range(len(data)):
        for col in range(len(data[0])):
            if (row, col) not in seen:
                stack = [(row, col)]
                seen.add((row, col))
                shape = {(row, col)}
                perimeter = 0
                while stack:
                    y, x = stack.pop()
                    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        ny, nx = y + dy, x + dx
                        if (
                                0 <= ny < len(data)
                                and 0 <= nx < len(data[0])
                                and data[ny][nx] == data[row][col]
                                and (ny, nx) not in seen
                        ):
                            stack.append((ny, nx))
                            seen.add((ny, nx))
                            shape.add((ny, nx))
                        elif (
                                not 0 <= ny < len(data)
                                or not 0 <= nx < len(data[0])
                                or data[ny][nx] != data[row][col]
                        ):
                            perimeter += 1
                # sides = get_path_sides(row, col, shape)
                # sides = get_sides_by_corners(shape)
                sides = get_sides_scan(shape)
                res_part1 += len(shape) * perimeter
                res_part2 += len(shape) * sides
    return res_part1, res_part2


def main():
    data = read_data('data/12.txt')
    start = time.monotonic()
    res1, res2 = solve(data)
    print('Part 1:', res1)
    print('Part 2:', res2)
    print(time.monotonic() - start)

if __name__ == '__main__':
    main()
