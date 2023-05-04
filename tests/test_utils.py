from src.utils import all_contains, check_if_url


def test_all_contains():
    assert all_contains([1, 2, 3], [1, 2, 3]) == True
    assert all_contains([1, 2, 3], []) == False
    assert all_contains([1, 2, 3, 4], [1, 2, 3]) == False
    assert all_contains([1, 2, 3], {}) == False


def test_check_if_url():
    assert check_if_url("https://example.com") == True
    assert check_if_url("http://example.com") == True
    assert check_if_url("example.com") == False


