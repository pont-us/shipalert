from main import extract_lat_lon


def test_extract_lat_lon():
    with open('/home/pont/test.html', 'r') as fh:
        content = fh.read()
    lat, lon = extract_lat_lon(content)
    assert 34.55643 == lat
    assert 27.91452 == lon

