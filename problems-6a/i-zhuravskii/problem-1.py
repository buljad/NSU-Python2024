import functools
import unittest


def cached(func):
    cache = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, frozenset(kwargs.items()))
        if key in cache:
            return cache[key]
        else:
            result = func(*args, **kwargs)
            cache[key] = result
            return result

    return wrapper


global state


@cached
def increment_counter(x):
    global state
    state += x
    return state


class TestCachedDecorator(unittest.TestCase):
    def test_cached_function_with_positional_args(self):
        @cached
        def add(a, b):
            return a + b

        self.assertEqual(add(1, 2), 3)
        self.assertEqual(add(1, 2), 3)

    def test_cached_function_with_keyword_args(self):
        @cached
        def multiply(a, b, c=1):
            return a * b * c

        self.assertEqual(multiply(2, 3), 6)
        self.assertEqual(multiply(2, 3, c=4), 24)
        self.assertEqual(multiply(2, 3, c=4), 24)

    def test_cached_function_with_unhashable_args(self):
        @cached
        def concat(a, b):
            return a + b

        with self.assertRaises(TypeError):
            concat([1, 2], [3, 4])

    def test_cached_function_with_different_args(self):
        @cached
        def subtract(a, b):
            return a - b

        self.assertEqual(subtract(5, 3), 2)
        self.assertEqual(subtract(10, 7), 3)
        self.assertEqual(subtract(5, 3), 2)

    def test_cached_function_with_kwargs_order(self):
        @cached
        def multiply(a, b, c=1, d=1):
            return a * b * c * d

        self.assertEqual(multiply(2, 3, c=4, d=5), 120)
        self.assertEqual(multiply(2, 3, d=5, c=4), 120)

    def test_side_effect(self):
        global state
        state = 0

        result = increment_counter(1)
        self.assertEqual(result, 1)
        self.assertEqual(state, 1)

        result = increment_counter(1)
        self.assertEqual(result, 1)
        self.assertEqual(state, 1)

    def test_named_arguments(self):
        @cached
        def sub(a, b):
            return a - b

        result = sub(b=5, a=10)
        self.assertEqual(result, 5)

        result = sub(10, 5)
        self.assertEqual(result, 5)
