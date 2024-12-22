import time
from collections import defaultdict, deque


def read_data(file_path: str) -> list:
    with open(file_path) as f:
        data = list(map(int, f.read().split('\n')))
    return data

def get_secret_num(num):
    num ^= num << 6
    num &= 0xFFFFFF
    num ^= num >> 5
    num &= 0xFFFFFF
    num ^= num << 11
    num &= 0xFFFFFF
    return num

def solve_part1(data, steps):
    res = 0
    for secret_num in data:
        for _ in range(steps):
            secret_num = get_secret_num(secret_num)
        res += secret_num
    return res

def solve_part2(data, steps):
    res = defaultdict(dict)
    for buyer_id, secret_num in enumerate(data):
        pre_price = secret_num % 10
        window = deque(maxlen=4)
        for _ in range(steps):
            secret_num = get_secret_num(secret_num)
            cur_price = secret_num % 10
            delta = cur_price - pre_price
            window.append(delta)
            if len(window) == 4:
                combination = tuple(window)
                if combination not in res:
                    res[combination][buyer_id] = cur_price
                elif buyer_id not in res[combination]:
                    res[combination][buyer_id] = cur_price
            pre_price = cur_price

    best_revenue = 0
    for buyers in res.values():
        best_revenue = max(
            best_revenue,
            sum(r for r in buyers.values())
        )
    return best_revenue

def main():
    # data = read_data('data/test.txt')
    data = read_data('data/22.txt')

    start = time.monotonic()
    res = solve_part1(data, 2000)
    print('Part 1:', res) # 19458130434
    print(time.monotonic() - start)

    res = solve_part2(data, 2000)
    print('Part 2:', res) # 2130
    print(time.monotonic() - start)

if __name__ == '__main__':
    main()
