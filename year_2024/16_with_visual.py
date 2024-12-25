import heapq
import time

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm


def read_data(file_path: str) -> dict:
    with open(file_path) as f:
        lines = f.readlines()
    data = {'maze': [], 'start': (0, 0), 'end': (0, 0)}
    for row, line in enumerate(lines):
        line = line.strip()
        map_line = []
        for col, char in enumerate(line):
            if char == 'S':
                data['start'] = (row, col)
                char = '.'
            elif char == 'E':
                data['end'] = (row, col)
                char = '.'
            map_line.append(char)
        line = map_line
        data['maze'].append(line)
    return data


def solve_part1(data):
    MOVES = (
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0),
    )
    y, x = data['start']
    end, maze = data['end'], data['maze']
    heap = [(0, y, x, 0)]
    seen = {
        (y, x),
    }

    ###
    fig, ax = plt.subplots(figsize=(len(maze), len(maze[0])))
    ax.imshow(np.zeros_like(maze, dtype=int), cmap='Greys', vmin=0, vmax=1)
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            ax.text(
                j,
                i,
                maze[i][j],
                color='black',
                ha='center',
                va='center',
                fontsize=10,
            )
    norm = mcolors.Normalize(vmin=0, vmax=10_000)
    cmap = cm.get_cmap('Greens')
    step_interval = 100
    step_counter = 0
    ###

    while heap:
        score, y, x, direction = heapq.heappop(heap)

        ###
        color = cmap(norm(score))
        step_counter += 1
        if step_counter >= step_interval:
            fig.canvas.draw()
            plt.pause(0.1)
            step_counter = 0
        ###

        if (y, x) == end:
            plt.show()
            return score
        for new_direction, (dy, dx) in enumerate(MOVES):
            ny, nx = y + dy, x + dx
            if (maze[ny][nx] == '.' and (ny, nx) not in seen) or (
                ny,
                nx,
            ) == end:
                ###
                ax.plot([x, nx], [y, ny], color=color, linewidth=10)
                ###
                rotate = abs(new_direction - direction)
                add_score = 1 + 1000 * (rotate if not rotate % 2 else 1)
                heapq.heappush(
                    heap, (score + add_score, ny, nx, new_direction)
                )
                seen.add((ny, nx))


def main():
    start = time.monotonic()
    data = read_data('data/test.txt')
    # data = read_data('16.txt')
    res = solve_part1(data)
    print('Part 1:', res)
    # res = solve_part2(data)
    # print('Part 2:', res)
    print(time.monotonic() - start)


if __name__ == '__main__':
    main()
