from src.to_string import to_string


@to_string
class JustStrings:
    just_string = 'Hello I am Just a string'
    x = 'hi'


@to_string
class JustNumbers:
    y = 4
    z = 123.67
    x = 9999999999.0000199


@to_string
class JustLists:
    a = []
    b = [1, 2, 3, 4]
    c = ['a', 'b', 'c', 'd', 'e']


@to_string
class JustTuples:
    i = ()
    j = (1, 2, 3, 4)
    k = ('a', 'b', 'c', 'd', 'e')


@to_string
class JustDicts:
    x = {
        'a': 3,
        'b': 4,
        'c': 'this',
        'd': {
            'nested': 3,
            'dict': 6
        }
    }


@to_string
class EmptyClass:
    pass


@to_string
class EverythingClass:
    just_string = JustStrings()
    just_numbers = JustNumbers()
    just_lists = JustLists()
    just_tuples = JustTuples()
    just_dicts = JustDicts()
    empty_class = EmptyClass()


def test_to_string_with_string_class():
    just_string = JustStrings()
    assert just_string.__str__() == '{just_string = Hello I am Just a string}, {x = hi}'


def test_to_string_with_numbers_class():
    just_numbers = JustNumbers()
    assert just_numbers.__str__() == '{x = 9999999999.00002}, ' \
                                     '{y = 4}, ' \
                                     '{z = 123.67}'


def test_to_string_with_lists_class():
    just_lists = JustLists()
    assert just_lists.__str__() == '{a = []}, ' \
                                   '{b = [1, 2, 3, 4]}, ' \
                                   '{c = [a, b, c, d, e]}'


def test_to_string_with_tuples_class():
    just_tuples = JustTuples()
    assert just_tuples.__str__() == '{i = []}, ' \
                                    '{j = [1, 2, 3, 4]}, ' \
                                    '{k = [a, b, c, d, e]}'


def test_to_string_with_dicts_class():
    just_dicts = JustDicts()
    assert just_dicts.__str__() == '{x = a : 3, b : 4, c : this, d : {\'nested\': 3, \'dict\': 6}}'


def test_to_string_with_empty_class():
    empty_class = EmptyClass()
    assert empty_class.__str__() == ''


def test_to_string_with_everything_class():
    everything_class = EverythingClass()
    assert everything_class.__str__() == '{empty_class = }, ' \
                                         '{just_dicts = {x = a : 3, b : 4, c : this, d : {\'nested\': 3, \'dict\': 6}}}, ' \
                                         '{just_lists = {a = []}, {b = [1, 2, 3, 4]}, {c = [a, b, c, d, e]}}, ' \
                                         '{just_numbers = {x = 9999999999.00002}, {y = 4}, {z = 123.67}}, ' \
                                         '{just_string = {just_string = Hello I am Just a string}, {x = hi}}, ' \
                                         '{just_tuples = {i = []}, {j = [1, 2, 3, 4]}, {k = [a, b, c, d, e]}}'


