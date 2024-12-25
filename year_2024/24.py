import collections
import time


def read_data(file_path: str) -> dict:
    with open(file_path) as f:
        wires, operations = f.read().split('\n\n')
    data = {'wires': [], 'operations': []}
    for line in wires.split('\n'):
        data['wires'].append(tuple(line.split(': ')))
    for line in operations.split('\n'):
        operation, output = line.split(' -> ')
        data['operations'].append(tuple([*operation.split(), output]))
    return data


def solve_part1(data):
    OPERATIONS = {
        'AND': lambda a, b: a & b,
        'OR': lambda a, b: a | b,
        'XOR': lambda a, b: a ^ b,
    }
    wires = {}
    for wire, value in data['wires']:
        wires[wire] = value == '1'
    queue = collections.deque([])
    z_list = []
    for l_operator, operation, r_operator, output in data['operations']:
        queue.append((l_operator, OPERATIONS[operation], r_operator, output))
        if output[0] == 'z' and output[1].isdigit():
            z_list.append(output)
    while queue:
        l_operator, operation, r_operator, output = queue.popleft()
        if all(op in wires for op in (l_operator, r_operator)):
            wires[output] = operation(wires[l_operator], wires[r_operator])
        else:
            queue.append((l_operator, operation, r_operator, output))
    res = []
    for z in sorted(z_list)[::-1]:
        res.append('1' if wires[z] else '0')
    res = int(''.join(res), 2)
    return res


def solve_part2(data):
    operations = []
    z_list = []
    operations_operators = collections.defaultdict(set)
    for l_operator, operation, r_operator, output in data['operations']:
        operations.append((l_operator, operation, r_operator, output))
        if output[0] == 'z':
            z_list.append(output)
        for operator in (l_operator, r_operator):
            operations_operators[operation].add(operator)
    z_list.sort()
    operators_with_or = operations_operators['OR']
    operators_with_or_only = (
        operators_with_or
        - operations_operators['AND']
        - operations_operators['XOR']
    )

    bad_nodes = set()
    for l_operator, operation, r_operator, output in operations:
        match operation:
            case 'XOR':
                is_any_xyz = any(
                    o[0] in {'x', 'y', 'z'}
                    for o in (l_operator, r_operator, output)
                )
                if not is_any_xyz or output in operators_with_or:
                    bad_nodes.add(output)
            case 'AND':
                is_first_bit = (
                    len({'x00', 'y00'} & {l_operator, r_operator}) != 0
                )
                if not is_first_bit and output not in operators_with_or_only:
                    bad_nodes._add(output)
            case 'AND' | 'OR':
                is_output_z_but_not_last = (
                    output[0] == 'z' and output != z_list[-1]
                )
                if is_output_z_but_not_last:
                    bad_nodes.add(output)
    return ','.join(sorted(bad_nodes))


def main():
    # data = read_data('data/test.txt')
    data = read_data('data/24.txt')

    start = time.monotonic()
    res = solve_part1(data)
    print('Part 1:', res)  # 56620966442854
    print(time.monotonic() - start)

    start = time.monotonic()
    res = solve_part2(data)
    print('Part 2:', res)  # chv,jpj,kgj,rts,vvw,z07,z12,z26
    print(time.monotonic() - start)


if __name__ == '__main__':
    main()
