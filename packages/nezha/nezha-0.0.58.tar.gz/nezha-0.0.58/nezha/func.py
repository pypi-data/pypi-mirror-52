from functools import wraps
from typing import Callable, Iterable, Mapping


def modify_positional_argument(index: int, val: str, action: str = 'replace', is_func_decorated: bool = True):
    """

    :param index: old positional argument index
    :param val:
    :param action:
        + if action == 'replace', old val -> val
        + if action == 'suffix', old val + val  -> val
        + if action == 'prefix', val + old val -> val
    :param is_func_decorated: if class method or instance method is decorated, self/cls should be passed.
    :return:

    example:

    @modify_positional_argument(0, 'xxxxx', action='prefix')
    def a(xx):
        print(xx)


    class A:

        @modify_positional_argument(0, 'xxxx', is_func_decorated=False)
        def a(self, x):
            print(x)
    """

    def action_factory(key: str) -> Callable:
        actions = {
            'replace': lambda old, new: new,
            'prefix': lambda old, new: new + old,
            'suffix': lambda old, new: old + new,
        }
        return actions[key]

    def decorate(func):
        @wraps(func)
        def wrap_method(self, *args, **kwargs):
            print(locals())
            old_val = args[index]
            print('old_val', old_val)
            new_args = list(args)
            new_args[index] = action_factory(action)(old_val, val)
            return func(self, *new_args, **kwargs)

        @wraps(func)
        def wrap_func(*args, **kwargs):
            print(locals())
            old_val = args[index]
            new_args = list(args)
            new_args[index] = action_factory(action)(old_val, val)
            return func(*new_args, **kwargs)

        return wrap_func if is_func_decorated else wrap_method

    return decorate


def modify_keyword_argument(new_pairs: Mapping, action: str = 'replace', is_func_decorated: bool = True):
    """

    :param new_pairs: new pair of keyword argument.
    :param action:
        + if action == 'replace', old val -> val
        + if action == 'suffix', old val + val  -> val
        + if action == 'prefix', val + old val -> val
    :param is_func_decorated: if class method or instance method is decorated, self/cls should be passed.
    :return:

    example:

    @modify_keyword_argument({'key': 4444}, action='prefix')
    def a(key=333):
        print(xx)


    class A:

        @modify_keyword_argument({'key': 4444}, action='prefix', is_func_decorated=False)
        def a(self, x):
            print(x)
    """

    def action_factory(key: str) -> Callable:
        actions = {
            'replace': lambda old, new: new,
            'prefix': lambda old, new: f'{new}{old}',
            'suffix': lambda old, new: f'{old}{new}',
        }
        return actions[key]

    def generate_new_pairs(new_pairs, kwargs, action):
        copied_kwargs = kwargs.copy()
        vals = {k: action_factory(action)(kwargs.get(k), new_val) for k, new_val in new_pairs.items()}
        copied_kwargs.update(vals)
        return copied_kwargs

    def decorate(func):
        @wraps(func)
        def wrap_method(self, *args, **kwargs):
            vals = generate_new_pairs(new_pairs, kwargs, action)
            return func(self, *args, **vals)

        @wraps(func)
        def wrap_func(*args, **kwargs):
            vals = generate_new_pairs(new_pairs, kwargs, action)
            return func(*args, **vals)

        return wrap_func if is_func_decorated else wrap_method

    return decorate


def loop(it: Iterable):
    while True:
        try:
            next(it)
        except StopIteration:
            break
