from main import extract_lat_lon, is_lon_in_range


def test_extract_lat_lon():
    with open('/home/pont/test.html', 'r') as fh:
        content = fh.read()
    lat, lon = extract_lat_lon(content)
    assert 34.55643 == lat
    assert 27.91452 == lon


def test_is_lon_in_range():
    assert is_lon_in_range(0, 10, 5)
    assert is_lon_in_range(-20, -5, -10)
    assert is_lon_in_range(170, -170, 180)
    assert is_lon_in_range(-180, -170, 185)
    assert not is_lon_in_range(0, 10, 20)
    assert not is_lon_in_range(170, -170, -169)
