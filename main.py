__author__ = 'bazarnik_p'

import csv
import logging
import pathlib
import requests
import wget
import urllib.request
from requests.exceptions import ConnectionError
from typing import Dict, List
from urllib.error import URLError

# For test file uploaded on local Apache server (on Windows path \Apache24\htdocs\files)
TARGET_URL = r'http://127.0.0.1/files/file.txt'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GetNameSurnameException(ValueError):
    pass


def download_csv_file_to_current_dir(target_url: str, output_file: str) -> None:
    print('\nRunning download_csv_file_to_current_dir')
    full_path_to_file = pathlib.Path(pathlib.Path.cwd() / output_file)
    if not full_path_to_file.exists():
        wget.download(target_url, out=str(full_path_to_file))


def get_name_surname_urllib(target_url: str) -> None:
    print('\nRunning get_name_surname_urllib')
    list_tmp = []
    try:
        lines = urllib.request.urlopen(target_url)
    except URLError as e:
        logger.error(f'URLError {e}')
    else:
        for line in lines:
            list_tmp.append(line.decode('utf-8').rstrip().split(';'))
        for item in list_tmp:
            print(f"Imie: {item[0]} Nazwisko: {item[1]}")


def get_name_surname_requests(target_url: str) -> None:
    print('\nRunning get_name_surname_requests')
    try:
        r = requests.get(target_url)

    except ConnectionError as e:
        logger.error(f'ConnectionError - {e}')
    else:
        if r.ok:
            for line in r.text.split('\n'):
                name, surname = line.rstrip().split(';')
                print(f"Imie: {name} Nazwisko: {surname}")
        else:
            raise GetNameSurnameException("Can't get name and surname")


def get_name_surname_csv_lib(file_name: str) -> None:
    print('\nRunning get_name_surname_csv_lib')
    try:
        with open(file_name, 'r') as csvfile:
            lines = csv.reader(csvfile, delimiter=";")
            for line in lines:
                print(f"Imie: {line[0]} Nazwisko: {line[1]}")
    except FileNotFoundError as e:
        logger.error(f'FileNotFoundError - {e}')


def get_dict_name_surname_csv_lib(file_name: str) -> List[Dict]:
    print('\nRunning get_dict_name_surname_csv_lib')
    try:
        with open(file_name, 'r') as csvfile:
            lines = csv.DictReader(csvfile, delimiter=";")
            dict_from_csv = list(lines)

            return dict_from_csv
    except FileNotFoundError as e:
        logger.error(f'FileNotFoundError - {e}')


def amount_of_value_repetitions_for_key(list_full_names: List[Dict], key: str, value: str) -> None:
    print('\nRunning amount_of_value_repetitions_for_key')
    amount = len([item for item in list_full_names if item[key] == value])
    print(f"amount of value: '{value}' for key: '{key}' equals {amount}")


if __name__ == '__main__':
    get_name_surname_requests(TARGET_URL)

    download_csv_file_to_current_dir(TARGET_URL, 'file.txt')

    get_name_surname_csv_lib('file.txt')

    get_name_surname_urllib(TARGET_URL)

    full_names = get_dict_name_surname_csv_lib('file_column_names.txt')

    amount_of_value_repetitions_for_key(full_names, 'name', 'imie1')
