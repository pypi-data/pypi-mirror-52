import functools


@functools.lru_cache()
def double_(value):
    print(f"doubling {value}")
    return value * 2


def test_demo_lru_cache(doubling_func):
    assert 4 == doubling_func(2)
    assert 4 == doubling_func(2)
    assert 6 == doubling_func(3)

