from hypothesis import given, strategies as st
from Binary_tree import DictDictionary


keys = st.integers()
values = st.text()
key_value_pairs = st.tuples(keys, values)


@given(pairs=st.lists(key_value_pairs))
def test_add_size(pairs):
    d = DictDictionary()
    unique_keys = set()
    for k, v in pairs:
        if k in unique_keys:
            expected_size = len(unique_keys)
        else:
            unique_keys.add(k)
            expected_size = len(unique_keys)
        d.add(k, v)
        assert d.size() == expected_size


@given(pairs=st.lists(key_value_pairs), key=st.integers())
def test_search(pairs, key):
    d = DictDictionary.from_list(pairs)
    expected = next(
        (v for k, v in reversed(pairs) if k == key), None
    )
    assert d.search(key) == expected


@given(pairs=st.lists(key_value_pairs), key=st.integers(), new_value=st.text())
def test_set(pairs, key, new_value):
    d = DictDictionary.from_list(pairs)
    original_exists = any(k == key for k, _ in pairs)
    d.set(key, new_value)
    if original_exists:
        assert d.search(key) == new_value
    else:
        assert d.search(key) is None


@given(pairs=st.lists(key_value_pairs), key=st.integers())
def test_remove(pairs, key):
    d = DictDictionary.from_list(pairs)
    original_size = d.size()
    unique_keys = {k for k, _ in pairs}
    d.remove(key)
    if key in unique_keys:
        assert d.size() == original_size - 1
        assert d.search(key) is None
    else:
        assert d.size() == original_size


@given(pairs=st.lists(key_value_pairs), value=st.text())
def test_member(pairs, value):
    d = DictDictionary.from_list(pairs)
    unique_pairs = {}
    for k, v in pairs:
        unique_pairs[k] = v  #
    values_in_dict = set(unique_pairs.values())
    assert d.member(value) == (value in values_in_dict)


@given(pairs=st.lists(key_value_pairs))
def test_from_list_to_list(pairs):
    d = DictDictionary.from_list(pairs)
    unique_pairs = {}
    for k, v in pairs:
        unique_pairs[k] = v
    sorted_pairs = sorted(unique_pairs.items(), key=lambda x: x[0])
    assert d.to_list() == sorted_pairs


@given(pairs=st.lists(key_value_pairs))
def test_reverse(pairs):
    d = DictDictionary.from_list(pairs)
    expected = sorted(d.to_list(), key=lambda x: x[0], reverse=True)
    assert d.reverse() == expected


@given(pairs=st.lists(key_value_pairs))
def test_filter(pairs):
    d = DictDictionary.from_list(pairs)
    filtered = d.filter(lambda k, v: k % 2 == 0)
    expected = [(k, v) for k, v in d.to_list() if k % 2 == 0]
    assert filtered == expected


@given(pairs=st.lists(key_value_pairs))
def test_map(pairs):
    d = DictDictionary.from_list(pairs)
    mapped = d.map(lambda k, v: (k + 1, v.upper()))
    expected = [(k + 1, v.upper()) for k, v in d.to_list()]
    assert mapped == expected


@given(pairs=st.lists(key_value_pairs))
def test_reduce(pairs):
    d = DictDictionary.from_list(pairs)
    sum_keys = d.reduce(lambda acc, k, v: acc + k, 0)
    expected = sum(k for k, _ in d.to_list())
    assert sum_keys == expected


@given(pairs=st.lists(key_value_pairs))
def test_iterator(pairs):
    d = DictDictionary.from_list(pairs)
    via_iterator = list(iter(d))
    assert via_iterator == d.to_list()


def test_empty():
    d = DictDictionary.empty()
    assert d.size() == 0
    assert d.to_list() == []


@given(pairs1=st.lists(key_value_pairs), pairs2=st.lists(key_value_pairs))
def test_concat(pairs1, pairs2):
    d1 = DictDictionary.from_list(pairs1)
    d2 = DictDictionary.from_list(pairs2)
    original_d1 = d1.to_list()
    d1.concat(d2)
    combined = dict(original_d1 + d2.to_list())
    expected = sorted(combined.items(), key=lambda x: x[0])
    assert d1.to_list() == expected


@given(pairs1=st.lists(key_value_pairs), pairs2=st.lists(key_value_pairs),
       pairs3=st.lists(key_value_pairs))
def test_concat3(pairs1, pairs2, pairs3):
    d1 = DictDictionary.from_list(pairs1)
    d2 = DictDictionary.from_list(pairs2)
    d3 = DictDictionary.from_list(pairs3)
    d1.concat(d2)
    d1.concat(d3)
    result1 = d1.to_list()
    d1_new = DictDictionary.from_list(pairs1)
    d2_d3 = DictDictionary.from_list(pairs2)
    d2_d3.concat(d3)
    d1_new.concat(d2_d3)
    result2 = d1_new.to_list()
    assert result1 == result2


@given(pairs1=st.lists(key_value_pairs))
def test_monoid(pairs1):
    d1 = DictDictionary.from_list(pairs1)
    e = DictDictionary.from_list([])
    d1_copy = DictDictionary.from_list(pairs1)  # 备份 d1
    d1_copy.concat(e)
    assert d1_copy.to_list() == d1.to_list()
    e_copy = DictDictionary.from_list([])
    e_copy.concat(d1)
    assert e_copy.to_list() == d1.to_list()
