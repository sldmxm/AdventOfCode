import time

from utils.download_data import check_and_download_data


def read_data(file_path: str) -> str:
    with open(file_path) as f:
        data = f.read().strip()
    return data


def solve_part1(data: str, layer_wide: int, layer_tall: int) -> int:
    layer_len = layer_wide * layer_tall
    layers_num_counters: list[dict[str, int]] = [
        {} for _ in range(len(data) // layer_len)
    ]
    for i, char in enumerate(data):
        cur_layer_char_counter = layers_num_counters[i // layer_len]
        cur_layer_char_counter[char] = cur_layer_char_counter.get(char, 0) + 1
    min_zero = layer_len
    res = 0
    for cur_layer_char_counter in layers_num_counters:
        if (
            '0' not in cur_layer_char_counter
            or cur_layer_char_counter['0'] < min_zero
        ):
            min_zero = cur_layer_char_counter.get('0', 0)
            res = cur_layer_char_counter.get(
                '1', 0
            ) * cur_layer_char_counter.get('2', 0)
    return res


def solve_part2(
    data: str, layer_wide: int, layer_tall: int
) -> list[list[int]]:
    layer_len = layer_wide * layer_tall
    layer_count = len(data) // layer_len
    res_image = [[2] * layer_wide for _ in range(layer_tall)]
    for y in range(layer_tall):
        for x in range(layer_wide):
            pixel_num = y * layer_wide + x
            for layer in range(layer_count):
                pixel = data[layer * layer_len + pixel_num]
                if pixel != '2':
                    res_image[y][x] = int(pixel)
                    break

    ink = {0: '\033[30m█\033[0m', 1: '█', 2: ' '}
    for row in res_image:
        line = []
        for n in row:
            line.append(ink[n])
        print(''.join(line))
    return res_image


def main() -> None:
    data_file_path = None
    try:
        data_file_path = check_and_download_data(__file__)
    except Exception as e:
        print(f'ERROR: {e}')

    if data_file_path:
        data = read_data(data_file_path)

        start = time.monotonic()
        res1 = solve_part1(data, 25, 6)
        print('Part 1:', res1)
        print(time.monotonic() - start)

        start = time.monotonic()
        solve_part2(data, 25, 6)
        print(time.monotonic() - start)


if __name__ == '__main__':
    main()
