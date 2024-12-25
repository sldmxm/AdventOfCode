import collections


def read_data(file_path: str) -> (list[tuple[int]], list[list[int]]):
    rules = []
    updates = []
    is_rules = True
    with open(file_path) as f:
        for row in f:
            row = row.rstrip()
            if not row:
                is_rules = False
            else:
                if is_rules:
                    rules.append([int(n) for n in row.split('|')])
                else:
                    updates.append([int(n) for n in row.split(',')])
    return rules, updates


def generate_dependencies(rules: list[list[int]]) -> dict[int : set[int]]:
    blocked_by = {}
    for blocker, blocked in rules:
        blocked_by[blocked] = blocked_by.get(blocked, set()) | {blocker}
    return blocked_by


def check_update(update: list[int], blocked_by: dict[int : set[int]]) -> bool:
    seen = set()
    update_set = set(update)
    for page in update:
        if page in blocked_by and (blocked_by[page] - seen) & update_set:
            return False
        seen.add(page)
    return True


def fix_update(
    update: list[int], blocked_by: dict[int : set[int]]
) -> list[int]:
    update_set = set(update)
    lock_count = [0] * len(update)
    lockers = {}
    queue = collections.deque([])
    for i, page in enumerate(update):
        blockers = blocked_by.get(page, set()) & update_set
        if blockers:
            lock_count[i] = len(blockers)
            for blocker in blockers:
                lockers[blocker] = lockers.get(blocker, []) + [i]
        else:
            queue.append(page)
    res = []
    while queue:
        page = queue.popleft()
        res.append(page)
        if page in lockers:
            for locked in lockers[page]:
                lock_count[locked] -= 1
                if lock_count[locked] == 0:
                    queue.append(update[locked])
    return res


if __name__ == '__main__':
    rules, updates = read_data('data/05_input.txt')
    dependencies = generate_dependencies(rules)
    part1_res = part2_res = 0
    for update in updates:
        if check_update(update, dependencies):
            part1_res += update[len(update) // 2]
        else:
            update = fix_update(update, dependencies)
            part2_res += update[len(update) // 2]
    print(part1_res)
    print(part2_res)
