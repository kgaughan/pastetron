from pastetron.pagination import paginator


def test_paginator():
    tests = (
        (1, 13, 2, [1, 2, 3, None, 13]),
        (2, 13, 2, [1, 2, 3, 4, None, 13]),
        (3, 13, 2, [1, 2, 3, 4, 5, None, 13]),
        (4, 13, 2, [1, 2, 3, 4, 5, 6, None, 13]),
        (5, 13, 2, [1, None, 3, 4, 5, 6, 7, None, 13]),
        (6, 13, 2, [1, None, 4, 5, 6, 7, 8, None, 13]),
        (7, 13, 2, [1, None, 5, 6, 7, 8, 9, None, 13]),
        (8, 13, 2, [1, None, 6, 7, 8, 9, 10, None, 13]),
        (9, 13, 2, [1, None, 7, 8, 9, 10, 11, None, 13]),
        (10, 13, 2, [1, None, 8, 9, 10, 11, 12, 13]),
        (11, 13, 2, [1, None, 9, 10, 11, 12, 13]),
        (12, 13, 2, [1, None, 10, 11, 12, 13]),
        (13, 13, 2, [1, None, 11, 12, 13]),
    )
    for page, max_pages, buffer_size, expected in tests:
        got = list(paginator(page, max_pages, buffer_size))
        assert got == expected
