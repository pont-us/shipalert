#!/usr/bin/env python3

from typing import Tuple, List
from bs4 import BeautifulSoup
from bs4.element import Tag
import yaml
import argparse
import requests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('config', metavar='YAML_file', type=str)
    args = parser.parse_args()
    with open(args.config, 'r') as fh:
        config = yaml.safe_load(fh)

    content = fetch_page_content(config['vessel_id'])
    lat, lon = extract_lat_lon(content)
    lon_min, lat_min, lon_max, lat_max = config['bbox']
    if lat_min <= lat <= lat_max and \
            lon_min <= lon <= lon_max:
        print('Yes!')
    else:
        print('No!')


def fetch_page_content(vessel_id: str) -> str:
    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) ' \
                 'Gecko/20100101 Firefox/96.0'
    r = requests.get(f'https://www.vesselfinder.com/vessels/{vessel_id}',
                     headers={'user-agent': user_agent})
    return r.text


def extract_lat_lon(page_content: str) -> Tuple[float, float]:
    soup = BeautifulSoup(page_content, 'html.parser')
    lat = extract_first_float(soup.find_all(class_='coordinate lat'))
    lon = extract_first_float(soup.find_all(class_='coordinate lon'))
    return lat, lon


def extract_first_float(tags: List[Tag]) -> float:
    for tag in tags:
        content = tag.contents[0]
        try:
            # noinspection PyTypeChecker
            return float(content)
        except ValueError:
            pass
    raise ValueError(f'No valid floats in {tags}')


if __name__ == '__main__':
    main()
