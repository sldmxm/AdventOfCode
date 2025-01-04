import time
from typing import Any

from utils.download_data import download_data


def read_data(
    file_path: str,
) -> dict[str, list[Any]]:
    with open(file_path) as f:
        lines = f.readlines()
    data = {}
    for line in lines:
        recipe, result = line.strip().split(' => ')
        ingredients = [ing.split() for ing in recipe.split(', ')]
        res_quantity, res_name = result.split()
        reaction = [
            int(res_quantity),
            tuple((int(q), n) for q, n in ingredients),
        ]
        data[res_name] = reaction
    return data


def solve_part1(
    data: dict[str, list[Any]],
    fuel_amount: int = 1,
    leftovers_ore: int = 0,
) -> int:
    needs = {'FUEL': fuel_amount}
    leftovers = {'ORE': leftovers_ore}
    ore_required = 0

    while needs:
        chemical, required_amount = needs.popitem()

        if chemical in leftovers:
            usable = min(required_amount, leftovers[chemical])
            required_amount -= usable
            leftovers[chemical] -= usable
            if leftovers[chemical] == 0:
                del leftovers[chemical]

        if required_amount == 0:
            continue

        if chemical == 'ORE':
            ore_required += required_amount
            continue

        reaction_output, ingredients = data[chemical]
        reactions_needed = -(-required_amount // reaction_output)
        leftover = reactions_needed * reaction_output - required_amount
        if leftover > 0:
            leftovers[chemical] = leftovers.get(chemical, 0) + leftover

        for amount, ing_chemical in ingredients:
            needs[ing_chemical] = (
                needs.get(ing_chemical, 0) + amount * reactions_needed
            )

    return ore_required


def solve_part2(data: dict[str, list[Any]]) -> int:
    ORE_AMOUNT = 10**12
    left = ORE_AMOUNT // solve_part1(data)
    right = left * 2
    while left <= right:
        mid = (left + right) // 2
        if solve_part1(data, mid, ORE_AMOUNT) > 0:
            right = mid - 1
        else:
            left = mid + 1
    return right


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
