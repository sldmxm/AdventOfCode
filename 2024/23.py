import collections
import heapq
import time

def read_data(file_path: str) -> list:
    with open(file_path) as f:
        lines = f.readlines()
    data = []
    for line in lines:
        data.append(tuple(line.strip().split('-')))
    return data

def solve_part1(data):
    connections = collections.defaultdict(set)
    for left, right in data:
        connections[left].add(right)
        connections[right].add(left)

    res = set()
    for root, nodes in connections.items():
        if len(nodes) >= 2 and root[0] == 't':
            cur = set(nodes)
            for second_node in nodes:
                cur.remove(second_node)
                if third_nodes := cur & connections[second_node]:
                    for third_node in third_nodes:
                        res.add(tuple(sorted([root, second_node, third_node])))
    return len(res)

def solve_part2(data):
    connections = collections.defaultdict(set)
    for left, right in data:
        connections[left].add(right)
        connections[right].add(left)

    res = tuple()

    for root, nodes in connections.items():
        direct_connected_nodes = {root}
        connections_to_check = []
        for node in nodes:
            common_links = len(connections[node] & nodes)
            heapq.heappush(connections_to_check, (-common_links, node))
        while connections_to_check:
            _, node = heapq.heappop(connections_to_check)
            if connections[node] & direct_connected_nodes == direct_connected_nodes:
                direct_connected_nodes.add(node)
        if len(direct_connected_nodes) > len(res):
            res = tuple(direct_connected_nodes)
    return ','.join(sorted(res))


def find_max_clique(data):
    def bron_kerbosch(R, P, X, graph, max_clique):
        if not P and not X:
            if len(R) > len(max_clique[0]):
                max_clique[0] = list(R)
            return
        u = next(iter(P.union(X))) if P or X else None
        for v in P - graph[u]:
            bron_kerbosch(
                R.union({v}),
                P.intersection(graph[v]),
                X.intersection(graph[v]),
                graph,
                max_clique
            )
            P.remove(v)
            X.add(v)

    connections = collections.defaultdict(set)
    for left, right in data:
        connections[left].add(right)
        connections[right].add(left)
    R, P, X = set(), set(connections.keys()), set()
    max_clique = [[]]
    bron_kerbosch(R, P, X, connections, max_clique)
    return ','.join(sorted(max_clique[0]))

def main():
    # data = read_data('data/test.txt')
    data = read_data('data/23.txt')

    start = time.monotonic()
    res = solve_part1(data)
    print('Part 1:', res)
    print(time.monotonic() - start)

    start = time.monotonic()
    res = solve_part2(data)
    print('Part 2 by me:', res)
    print(time.monotonic() - start) # 0.008

    start = time.monotonic()
    res = find_max_clique(data)
    print('Part 2 by Bron-Kerbosch:', res)
    print(time.monotonic() - start) # 0.004

if __name__ == '__main__':
    main()
