#!/usr/bin/env python3

"""Check whether a vessel is within a specified bounding box

Copyright 2022 by Pontus Lurcock
Released under the MIT license; see the file LICENSE.txt for details.
"""

from typing import Tuple, List
from bs4 import BeautifulSoup
from bs4.element import Tag
import argparse
import requests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('vessel', metavar='Vessel-ID', type=str,
                        help='As it appears in the vesselfinder.com URL')
    parser.add_argument('bbox', metavar='Bounding-box', type=str,
                        help='decimal degrees. Format: '
                             '<min-lon>,<min-lat>,<max-lon>,<max-lat>')
    parser.add_argument('--cronmode', action='store_true',
                        help='Only write output if vessel is in bbox.')
    args = parser.parse_args()

    content = fetch_page_content(args.vessel)
    lat, lon = extract_lat_lon(content)
    lon_min, lat_min, lon_max, lat_max = tuple(map(float, args.bbox.split(',')))
    vessel_inside = \
        lat_min <= lat <= lat_max and is_lon_in_range(lon_min, lon_max, lon)
    if vessel_inside or not args.cronmode:
        print(f'{args.vessel} is at {lat} N {lon} E, '
              f'{"in" if vessel_inside else "out"}side {args.bbox}')


def fetch_page_content(vessel_id: str) -> str:
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
                 'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 'Chrome/96.0.4664.110 Safari/537.36'
    response = requests.get(
        f'https://www.vesselfinder.com/vessels/{vessel_id}',
        headers={'user-agent': user_agent}
    )
    return response.text


def extract_lat_lon(page_content: str) -> Tuple[float, float]:
    soup = BeautifulSoup(page_content, 'html.parser')
    lat = extract_first_float(soup.find_all(class_='coordinate lat'))
    lon = extract_first_float(soup.find_all(class_='coordinate lon'))
    return lat, lon


def is_lon_in_range(lon_min: float, lon_max: float, lon: float) -> bool:
    lon_min_norm = (lon_min + 360) % 360
    lon_max_norm = (lon_max + 360) % 360
    lon_norm = (lon + 360) % 360
    if lon_min_norm <= lon_max_norm:
        return lon_min_norm <= lon_norm <= lon_max_norm
    else:
        return lon_norm < lon_max_norm or lon_norm > lon_min_norm


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
