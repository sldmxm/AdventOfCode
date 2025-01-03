import os
import time
from dataclasses import dataclass, field

from utils.download_data import download_data
from year_2019.intcode import IntcodeComp, ProgramStatus

TILES_TYPE = {0: ' ', 1: '█', 2: '▒', 3: '=', 4: '●'}


@dataclass
class GameData:
    field: dict[tuple[int, int], int] = field(default_factory=dict)
    score: int = 0
    ball: tuple[int, int] | None = None
    paddle: tuple[int, int] | None = None


def read_data(file_path: str) -> str:
    with open(file_path) as f:
        data = f.read().strip()
    return data


def solve_part1(data: str) -> int:
    comp = IntcodeComp(data)
    comp.run_whole_code()
    output = comp.get_output()
    tiles = {}
    max_x, max_y = 0, 0
    for i in range(0, len(output), 3):
        x, y, t = output[i : i + 3]
        tiles[(x, y)] = t
        max_x = max(max_x, x)
        max_y = max(max_y, y)
    res = 0
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            res += 1 if tiles.get((x, y), 0) == 2 else 0
    return res


def solve_part2(data: str) -> int:
    def parse_output(output: list[int]) -> GameData:
        res = GameData()
        for i in range(0, len(output), 3):
            x, y, t = output[i : i + 3]
            res.field[(x, y)] = t
            if (x, y) == (-1, 0):
                res.score = t
            elif t == 4:
                res.ball = (x, y)
            elif t == 3:
                res.paddle = (x, y)
        return res

    def render_screen() -> None:
        screen = []
        for y in range(max_y + 1):
            line = []
            for x in range(max_x + 1):
                line.append(TILES_TYPE[game_data.field.get((x, y), 0)])
            screen.append(''.join(line))
        os.system('clear')
        print('\n'.join(screen))
        print(game_data.score)

    comp = IntcodeComp(data)
    max_x, max_y = 0, 0
    new_input: list[int] = []
    while True:
        comp.run_whole_code(new_input)
        game_data = parse_output(comp.get_output())
        if max_x == 0:
            max_x, max_y = (
                max(x for (x, y) in game_data.field),
                max(y for (x, y) in game_data.field),
            )

        render_screen()
        time.sleep(0.2)

        if comp.get_status() == ProgramStatus.DONE:
            return game_data.score

        if game_data.ball and game_data.paddle:
            if game_data.ball[0] < game_data.paddle[0]:
                new_input = [-1]
            elif game_data.ball[0] > game_data.paddle[0]:
                new_input = [1]
            else:
                new_input = [0]


def main() -> None:
    data_file_path = None
    try:
        data_file_path = download_data(__file__)
    except Exception as e:
        print(f'ERROR: {e}')

    if data_file_path:
        data = read_data(data_file_path)

        start = time.monotonic()
        res1 = solve_part1(data)
        print('Part 1:', res1)
        print(time.monotonic() - start)

        start = time.monotonic()
        res2 = solve_part2(data)
        print('Part 2:', res2)
        print(time.monotonic() - start)


if __name__ == '__main__':
    main()
