import time

from utils.download_data import download_data


def read_data(file_path: str) -> list[str]:
    with open(file_path) as f:
        data = [line.strip() for line in f.readlines()]
    return data


def shuffle(data: list[str], deck_size: int = 10007) -> list[int]:
    deck = list(range(deck_size))
    for technique in data:
        if technique == 'deal into new stack':
            deck.reverse()
        elif technique.startswith('deal with increment'):
            num = int(technique.split()[-1])
            new_deck = [0] * deck_size
            pos = 0
            for card in deck:
                new_deck[pos] = card
                pos = (pos + num) % deck_size
            deck = new_deck
        elif technique.startswith('cut'):
            num = int(technique.split()[-1])
            deck = deck[num:] + deck[:num]
    return deck


def solve_part1(data: list[str]) -> int:
    return shuffle(data).index(2019)


def solve_part2(data: list[str]) -> int:
    def parse(L: int) -> tuple[int, int]:
        a, b = 1, 0
        for technique in data[::-1]:
            if technique == 'deal into new stack':
                a = -a
                b = L - b - 1
                continue
            elif technique.startswith('deal with increment'):
                num = int(technique.split()[-1])
                z = pow(num, L - 2, L)
                a = a * z % L
                b = b * z % L
                continue
            elif technique.startswith('cut'):
                num = int(technique.split()[-1])
                b = (b + num) % L
                continue
        return a, b

    def poly_pow(a: int, b: int, m: int, N: int) -> tuple[int, int]:
        if m == 0:
            return 1, 0
        if m % 2 == 0:
            return poly_pow(a * a % N, (a * b + b) % N, m // 2, N)
        else:
            c, d = poly_pow(a, b, m - 1, N)
            return a * c % N, (a * d + b) % N

    def shuffle2(L: int, N: int, pos: int) -> int:
        a, b = parse(L)
        a, b = poly_pow(a, b, N, L)
        return (pos * a + b) % L

    L = 119315717514047
    N = 101741582076661

    return shuffle2(L, N, 2020)


def main() -> None:
    data_file_path = None
    try:
        data_file_path = download_data(__file__)
    except Exception as e:
        print(f'ERROR: {e}')

    if data_file_path:
        data = read_data(data_file_path)

        start = time.monotonic()
        res1 = solve_part1(data)
        print('Part 1:', res1)
        print(time.monotonic() - start)

        start = time.monotonic()
        res2 = solve_part2(data)
        print('Part 2:', res2)  # > 67925815117695, == 71047285772808
        print(time.monotonic() - start)


if __name__ == '__main__':
    main()
