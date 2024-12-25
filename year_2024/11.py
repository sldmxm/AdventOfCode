import collections
import time


def read_data(file_path: str) -> list[int]:
    with open(file_path) as f:
        row = f.readline()
    data = [int(n) for n in row.rstrip().split()]
    return data


def solve(data, blinks) -> int:
    counter = collections.Counter(data)
    for _ in range(blinks):
        next_counter = {}
        for num in counter:
            if num == 0:
                next_counter[1] = next_counter.get(1, 0) + counter[0]
            elif not len(str(num)) % 2:
                half_length = len(str(num)) // 2
                left = int(str(num)[:half_length])
                right = int(str(num)[half_length:])
                next_counter[left] = next_counter.get(left, 0) + counter[num]
                next_counter[right] = next_counter.get(right, 0) + counter[num]
            else:
                next_counter[num * 2024] = (
                    next_counter.get(num * 2024, 0) + counter[num]
                )
        counter = next_counter.copy()
    return sum(counter.values())


def main():
    data = read_data('data/11.txt')
    start = time.monotonic()
    res1 = solve(data, 25)
    res2 = solve(data, 75)
    print('Part 1:', res1)
    print('Part 2:', res2)
    print(time.monotonic() - start)


if __name__ == '__main__':
    main()
