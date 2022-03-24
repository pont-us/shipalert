import os

from shipalert.shipalert import extract_lat_lon, is_lon_in_range

cwd = os.path.abspath(os.path.dirname(__file__))


def test_extract_lat_lon():
    with open(os.path.join(cwd, 'sample_input.html'), 'r') as fh:
        content = fh.read()
    lat, lon = extract_lat_lon(content)
    assert 34.55643 == lat
    assert 27.91452 == lon


def test_is_lon_in_range():
    assert is_lon_in_range(0, 10, 5)
    assert is_lon_in_range(-20, -5, -10)
    assert is_lon_in_range(170, -170, 180)
    assert is_lon_in_range(-180, -170, 185)
    assert is_lon_in_range(150, 100, 150)
    assert is_lon_in_range(150, 100, 100)
    assert not is_lon_in_range(150, 100, 100.1)
    assert not is_lon_in_range(150, 100, 149.9)
    assert not is_lon_in_range(0, 10, 20)
    assert not is_lon_in_range(170, -170, -169)
