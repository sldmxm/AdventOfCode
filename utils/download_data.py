import os

import requests
from dotenv import load_dotenv

load_dotenv()


def get_url(year: str, day: str) -> str:
    return f'https://adventofcode.com/{year}/day/{day}/input'


def get_year_day(py_path: str) -> tuple[str, str]:
    _, year, _, day = py_path.split('/')[-1].split('.')[0].split('_')
    return year, day


def check_and_download_data(py_path: str) -> str:
    year, day = get_year_day(py_path)
    file_path = f'data/year{year}day{day}.txt'

    cookie_value = os.getenv('COOKIE')
    if not cookie_value:
        raise ValueError(
            'Cookie not found. '
            'Check that the COOKIE variable is specified in the .env file.'
        )

    if not os.path.exists(file_path):
        print(f'{file_path} does not exist. Create and load data...')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        cookies = {'session_id': cookie_value}

        url = get_url(year, str(int(day)))
        response = requests.get(url, cookies=cookies)
        response.raise_for_status()

        with open(file_path, 'wb') as file:
            file.write(response.content[:-1])
        print(f'{file_path} file successfully uploaded.')
    else:
        print(f'{file_path} file is already there.')
    return file_path
