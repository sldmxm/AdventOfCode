def get_safe_count(data: list[list[int]], tolerance: bool) -> int:
    res = 0
    for row in data:
        dp_desc = [0] * (len(row) + 1)
        dp_asc = [0] * (len(row) + 1)
        dp_desc[1] = 1
        dp_asc[1] = 1
        max_len = 1
        for i in range(1, len(row)):
            dp_desc[i + 1] = max(
                (row[i - 1] > row[i]) * (1 <= abs(row[i - 1] - row[i]) <= 3) * dp_desc[i] + 1,
                ((row[i - 2] > row[i]) * (1 <= abs(row[i - 2] - row[i]) <= 3) * dp_desc[i - 1] + 1) if i > 1 else 1,
            )
            dp_asc[i + 1] = max(
                (row[i - 1] < row[i]) * (1 <= abs(row[i - 1] - row[i]) <= 3) * dp_asc[i] + 1,
                ((row[i - 2] < row[i]) * (1 <= abs(row[i - 2] - row[i]) <= 3) * dp_asc[i - 1] + 1) if i > 1 else 1,
            )
            max_len = max(max_len, dp_desc[i + 1], dp_asc[i + 1])
        res += max_len + tolerance >= len(row)
        if max_len + tolerance < len(row) and len(row) - len(set(row)) < 2:
            print(f'{row=} {dp_asc=} {dp_desc=}')
    return res

def read_data(file_path: str) -> list[list[int]]:
    res = []
    with open(file_path) as f:
        for row in f:
            data_row = [int(n) for n in row.split()]
            res.append(data_row)
    return res


if __name__ == '__main__':
    data = read_data('data/02_input.txt')
    print(get_safe_count(data, True))
