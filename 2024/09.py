import time

def read_data(file_path: str) -> dict:
    with open(file_path) as f:
        data = f.readlines()
    data = data[0].rstrip()
    return data

def solve(data):
    def checksum():
        return sum(
            i * filesystem[i] for i in range(len(filesystem))
            if filesystem[i] != '.'
        )

    filesystem = []
    files_idx_size = []
    free_idx_size = []
    data = [int(n) for n in data]
    for i in range(len(data)):
        if i % 2 == 0:
            files_idx_size.append((i // 2, len(filesystem), data[i]))
            filesystem.extend([i // 2] * data[i])
        else:
            free_idx_size.append((len(filesystem), data[i]))
            filesystem.extend(['.'] * data[i])

    filesystem_backup = filesystem[:]
    l, r = 0, len(filesystem) - 1
    while l < r:
        if filesystem[l] == '.' and filesystem[r] != '.':
            filesystem[l], filesystem[r] = filesystem[r], '.'
            l += 1
            r -= 1
        else:
            if filesystem[l] != '.':
                l += 1
            if filesystem[r] == '.':
                r -= 1
    checksum_part1 = checksum()

    filesystem = filesystem_backup
    for file, file_idx, file_size in files_idx_size[::-1]:
        for i, (free_idx, free_size) in enumerate(free_idx_size[:file]):
            if free_size >= file_size and file_idx > free_idx:
                filesystem[free_idx:free_idx + file_size] = [file] * file_size
                filesystem[file_idx:file_idx + file_size] = ['.'] * file_size
                free_idx_size[i] = (free_idx + file_size, free_size - file_size)
                break
    checksum_part2 = checksum()

    return checksum_part1, checksum_part2

def main():
    data = read_data('data/09_input.txt')
    start = time.monotonic()
    res1, res2 = solve(data,)
    print('Part 1:', res1)
    print('Part 2:', res2)
    print(time.monotonic() - start)

if __name__ == '__main__':
    main()
