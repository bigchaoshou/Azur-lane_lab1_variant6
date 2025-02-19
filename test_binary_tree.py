import pytest
from hypothesis import given, strategies as st, assume
from Binary_tree import BSTDictionary

keys = st.integers()
values = st.text()
key_value_pairs = st.tuples(keys, values)

# 测试 add 和 size 方法
@given(pairs=st.lists(key_value_pairs))
def test_add_size(pairs):
    d = BSTDictionary()
    unique_keys = set()
    for k, v in pairs:
        if k in unique_keys:
            expected_size = len(unique_keys)
        else:
            unique_keys.add(k)
            expected_size = len(unique_keys)
        d.add(k, v)
        assert d.size() == expected_size


# 测试 search 方法
@given(pairs=st.lists(key_value_pairs), key=st.integers())
def test_search(pairs, key):
    d = BSTDictionary.from_list(pairs)
    expected = next((v for k, v in reversed(pairs) if k == key), None)
    assert d.search(key) == expected


# 测试 set 方法
@given(pairs=st.lists(key_value_pairs), key=st.integers(), new_value=st.text())
def test_set(pairs, key, new_value):
    d = BSTDictionary.from_list(pairs)
    original_exists = any(k == key for k, _ in pairs)
    d.set(key, new_value)
    if original_exists:
        assert d.search(key) == new_value
    else:
        assert d.search(key) is None


# 测试 remove 方法
@given(pairs=st.lists(key_value_pairs), key=st.integers())
def test_remove(pairs, key):
    d = BSTDictionary.from_list(pairs)
    original_size = d.size()
    unique_keys = {k for k, _ in pairs}
    d.remove(key)
    if key in unique_keys:
        assert d.size() == original_size - 1
        assert d.search(key) is None
    else:
        assert d.size() == original_size


# 测试 member 方法
@given(pairs=st.lists(key_value_pairs), value=st.text())
def test_member(pairs, value):
    d = BSTDictionary.from_list(pairs)
    unique_pairs = {}
    for k, v in pairs:
        unique_pairs[k] = v  #
    values_in_dict = set(unique_pairs.values())
    assert d.member(value) == (value in values_in_dict)


# 测试 from_list 和 to_list 方法
@given(pairs=st.lists(key_value_pairs))
def test_from_list_to_list(pairs):
    d = BSTDictionary.from_list(pairs)
    unique_pairs = {}
    for k, v in pairs:
        unique_pairs[k] = v
    sorted_pairs = sorted(unique_pairs.items(), key=lambda x: x[0])
    assert d.to_list() == sorted_pairs


# 测试 reverse 方法
@given(pairs=st.lists(key_value_pairs))
def test_reverse(pairs):
    d = BSTDictionary.from_list(pairs)
    expected = sorted(d.to_list(), key=lambda x: x[0], reverse=True)
    assert d.reverse() == expected


# 测试 filter 方法
@given(pairs=st.lists(key_value_pairs))
def test_filter(pairs):
    d = BSTDictionary.from_list(pairs)
    filtered = d.filter(lambda k, v: k % 2 == 0)
    expected = [(k, v) for k, v in d.to_list() if k % 2 == 0]
    assert filtered == expected


# 测试 map 方法
@given(pairs=st.lists(key_value_pairs))
def test_map(pairs):
    d = BSTDictionary.from_list(pairs)
    mapped = d.map(lambda k, v: (k + 1, v.upper()))
    expected = [(k + 1, v.upper()) for k, v in d.to_list()]
    assert mapped == expected


# 测试 reduce 方法
@given(pairs=st.lists(key_value_pairs))
def test_reduce(pairs):
    d = BSTDictionary.from_list(pairs)
    sum_keys = d.reduce(lambda acc, k, v: acc + k, 0)
    expected = sum(k for k, _ in d.to_list())
    assert sum_keys == expected


# 测试迭代器
@given(pairs=st.lists(key_value_pairs))
def test_iterator(pairs):
    d = BSTDictionary.from_list(pairs)
    via_iterator = list(iter(d))
    assert via_iterator == d.to_list()


# 测试 empty 方法
def test_empty():
    d = BSTDictionary.empty()
    assert d.size() == 0
    assert d.to_list() == []


# 测试 concat 方法
@given(pairs1=st.lists(key_value_pairs), pairs2=st.lists(key_value_pairs))
def test_concat(pairs1, pairs2):
    d1 = BSTDictionary.from_list(pairs1)
    d2 = BSTDictionary.from_list(pairs2)
    d1.concat(d2)
    combined = {k: v for k, v in d1.to_list() + d2.to_list()}
    expected = sorted(combined.items(), key=lambda x: x[0])
    assert d1.to_list() == expected


if __name__ == "__main__":
    pytest.main()
