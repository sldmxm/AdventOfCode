import time


def is_number_ok_part1(num: int) -> bool:
    n = str(num)
    is_ok = False
    for i in range(1, len(n)):
        if n[i] < n[i - 1]:
            return False
        elif n[i] == n[i - 1]:
            is_ok = True
    return is_ok


def is_number_ok_part2(num: int) -> bool:
    n = str(num)
    repeat_counter = 1
    has_exact_double = False
    for i in range(1, len(n)):
        if n[i] < n[i - 1]:
            return False
        elif n[i] == n[i - 1]:
            repeat_counter += 1
        else:
            if repeat_counter == 2:
                has_exact_double = True
            repeat_counter = 1
    if repeat_counter == 2:
        has_exact_double = True
    return has_exact_double


def solve(data: str) -> tuple[int, int]:
    start, end = map(int, data.split('-'))
    count_part1, count_part2 = 0, 0
    for n in range(start, end):
        count_part1 += (is_ok_part1 := is_number_ok_part1(n))
        if is_ok_part1:
            count_part2 += is_number_ok_part2(n)
    return count_part1, count_part2


def main() -> None:
    data = '372037-905157'

    start = time.monotonic()
    res1, res2 = solve(data)
    print('Part 1:', res1)
    print('Part 2:', res2)
    print(time.monotonic() - start)


if __name__ == '__main__':
    main()
