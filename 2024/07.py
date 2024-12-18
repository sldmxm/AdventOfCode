import time

def read_data(file_path: str) -> list[list[int]]:
    data = []
    with open(file_path) as f:
        rows = f.readlines()
    for row in rows:
        res, parts = row.split(':')
        cur = [int(res)] + [int(n) for n in parts.split()]
        data.append(cur)
    return data

def dfs_solve(rows: list[list[int]]) -> (int, int):
    def check_dfs(goal, nums, operators):
        OPS = {
            '+': lambda a, b: a + b,
            '*': lambda a, b: a * b,
            '|': lambda a, b: int(str(a) + str(b)),
        }

        def _dfs(i, cur):
            if i == len(nums):
                return goal == cur
            for operation in operators:
                if _dfs(i + 1, OPS[operation](cur, nums[i])):
                    return True
            return False

        return _dfs(1, nums[0])

    solve1 = solve2 = 0
    for result, *parts in rows:
        if check_dfs(result, parts, '+*'):
            solve1 += result
            solve2 += result
        elif check_dfs(result, parts, '+*|'):
            solve2 += result
    return solve1, solve2

def fast_solve(rows: list[list[int]]) -> (int, int):
    def fast_check(goal, nums, concatenation):
        def is_concatenated(big_num, small_num):
            big_num, small_num = str(big_num), str(small_num)
            return big_num[-len(small_num):] == small_num

        def deconcatenation(big_num, small_num):
            big_num, small_num = str(big_num), str(small_num)
            return int(big_num[:-len(small_num)])

        def _helper(cur_goal, cur_nums):
            if len(cur_nums) == 1:
                return (
                    cur_goal == cur_nums[0]
                    or cur_goal - cur_nums[0] == 0
                )

            return (
                    cur_goal % cur_nums[-1] == 0
                    and _helper(cur_goal // cur_nums[-1], cur_nums[:-1])

                    or _helper(cur_goal - cur_nums[-1], cur_nums[:-1])

                    or concatenation and is_concatenated(cur_goal, cur_nums[-1])
                    and _helper(deconcatenation(cur_goal, cur_nums[-1]), cur_nums[:-1])
            )

        return _helper(goal, nums)

    solve1 = solve2 = 0
    for result, *parts in rows:
        if fast_check(result, parts, False):
            solve1 += result
            solve2 += result
        elif fast_check(result, parts, True):
            solve2 += result
    return solve1, solve2

def main():
    data = read_data('data/07_input.txt')
    for solve in (dfs_solve, fast_solve):
        start = time.monotonic()
        res1, res2 = solve(data)
        print(solve.__name__, time.monotonic() - start)
        print('Part 1:', res1)
        print('Part 2:', res2)

if __name__ == '__main__':
    main()
