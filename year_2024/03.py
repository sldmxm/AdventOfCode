import re


def get_sum_mul(data: str) -> int:
    res = 0
    for mul in re.findall(r'(mul\(\d+,\d+\))', data):
        multipliers = re.findall(r'\d+', mul)
        res += int(multipliers[0]) * int(multipliers[1])
    return res


def get_sum_mul_part2(data: str) -> int:
    res = 0
    is_turn_on = True
    pattern = r"(don't\(\))|(do\(\))|(mul\(\d+,\d+\))"
    for turn_off, turn_on, mul in re.findall(pattern, data):
        if turn_off:
            is_turn_on = False
        if turn_on:
            is_turn_on = True
        if mul:
            multipliers = re.findall(r'\d+', mul)
            res += int(multipliers[0]) * int(multipliers[1]) * is_turn_on
    return res


if __name__ == '__main__':
    with open('data/03_input.txt') as f:
        data = f.read()
    print(get_sum_mul(data))
    print(get_sum_mul_part2(data))
