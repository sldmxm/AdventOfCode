import time

from utils.download_data import download_data

PATTERN = (0, 1, 0, -1)


def read_data(file_path: str) -> str:
    with open(file_path) as f:
        data = f.read().strip()
    return data


def solve_part1(data: str, phases: int) -> str:
    inpt = [int(c) for c in data]
    output = []
    for _ in range(phases):
        for step in range(len(inpt)):
            pattern = [n for n in PATTERN for _ in range(step + 1)]
            pattern_idx = 1
            cur = 0
            for n in inpt:
                cur += n * pattern[pattern_idx]
                pattern_idx = (pattern_idx + 1) % len(pattern)
            output.append(abs(cur) % 10)
        inpt = output
        output = []
    return ''.join(map(str, inpt[:8]))


def solve_part2(data: str, phases: int) -> str | None:
    inpt = [int(c) for c in data]
    signal = inpt * 10000
    offset = int(data[:7])
    if offset > len(signal) // 2:
        relevant_signal = signal[offset:]
        for _ in range(phases):
            cumulative_sum = 0
            for i in range(len(relevant_signal) - 1, -1, -1):
                cumulative_sum += relevant_signal[i]
                relevant_signal[i] = abs(cumulative_sum) % 10
        return ''.join(map(str, relevant_signal[:8]))
    else:
        raise ValueError(
            'Offset must be in the second half of the signal, sorry.'
        )


def main() -> None:
    data_file_path = None
    try:
        data_file_path = download_data(__file__)
    except Exception as e:
        print(f'ERROR: {e}')

    if data_file_path:
        data = read_data(data_file_path)

        start = time.monotonic()
        res1 = solve_part1(data, 100)
        print('Part 1:', res1)
        print(time.monotonic() - start)

        start = time.monotonic()
        res2 = solve_part2(data, 100)
        print('Part 2:', res2)
        print(time.monotonic() - start)


if __name__ == '__main__':
    main()
