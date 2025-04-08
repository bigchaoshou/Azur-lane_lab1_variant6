from hypothesis import given, strategies as st
from Binary_tree import BinaryTreeDict, empty, cons, concat, length, member, remove, from_list, to_list

keys = st.integers()
values = st.text()
key_value_pairs = st.tuples(keys, values)


@given(pairs=st.lists(key_value_pairs))
def test_add_size(pairs):
    tree = empty()
    unique_keys = set()
    for k, v in pairs:
        if k in unique_keys:
            expected_size = len(unique_keys)
        else:
            unique_keys.add(k)
            expected_size = len(unique_keys)
        cons(k, v, tree)
        assert length(tree) == expected_size


@given(pairs=st.lists(key_value_pairs), key=keys)
def test_search(pairs, key):
    tree = from_list(pairs)
    expected = next((v for k, v in reversed(pairs) if k == key), None)
    assert tree.search(key) == expected


@given(pairs=st.lists(key_value_pairs), key=keys, new_value=values)
def test_set(pairs, key, new_value):
    tree = from_list(pairs)
    original_exists = any(k == key for k, _ in pairs)
    tree.add(key, new_value)
    if original_exists:
        assert tree.search(key) == new_value
    else:
        assert tree.search(key) == new_value


@given(pairs=st.lists(key_value_pairs), key=keys)
def test_remove(pairs, key):
    tree = from_list(pairs)
    original_size = length(tree)
    unique_keys = {k for k, _ in pairs}
    remove(tree, key)
    if key in unique_keys:
        assert length(tree) == original_size - 1
        assert tree.search(key) is None
    else:
        assert length(tree) == original_size


@given(pairs=st.lists(key_value_pairs))
def test_from_list_to_list(pairs):
    tree = from_list(pairs)
    unique_pairs = {}
    for k, v in pairs:
        unique_pairs[k] = v
    sorted_pairs = sorted(unique_pairs.items())
    assert to_list(tree) == sorted_pairs



@given(pairs=st.lists(key_value_pairs))
def test_filter(pairs):
    tree = from_list(pairs)
    original_items = to_list(tree)
    tree.filter(lambda k, v: k % 2 == 0)
    expected = [(k, v) for k, v in original_items if k % 2 == 0]
    assert to_list(tree) == expected


@given(pairs=st.lists(key_value_pairs))
def test_map(pairs):
    tree = from_list(pairs)
    expected = [(k + 1, v.upper()) for k, v in to_list(tree)]
    tree.map(lambda k, v: (k + 1, v.upper()))
    assert to_list(tree) == expected


@given(pairs=st.lists(key_value_pairs))
def test_reduce(pairs):
    tree = from_list(pairs)
    sum_keys = tree.reduce(lambda acc, k, v: acc + k, 0)
    expected = sum(k for k, _ in to_list(tree))
    assert sum_keys == expected


@given(pairs=st.lists(key_value_pairs))
def test_iterator(pairs):
    tree = from_list(pairs)
    via_iterator = list(iter(tree))
    assert via_iterator == [k for k, _ in to_list(tree)]


def test_empty():
    tree = empty()
    assert length(tree) == 0
    assert to_list(tree) == []


@given(pairs1=st.lists(key_value_pairs), pairs2=st.lists(key_value_pairs))
def test_concat(pairs1, pairs2):
    tree1 = from_list(pairs1)
    tree2 = from_list(pairs2)
    original_tree1 = to_list(tree1)
    concat(tree1, tree2)
    combined = dict(original_tree1 + to_list(tree2))
    expected = sorted(combined.items())
    assert to_list(tree1) == expected


@given(pairs1=st.lists(key_value_pairs),
       pairs2=st.lists(key_value_pairs),
       pairs3=st.lists(key_value_pairs))
def test_concat3(pairs1, pairs2, pairs3):
    tree1 = from_list(pairs1)
    tree2 = from_list(pairs2)
    tree3 = from_list(pairs3)

    #  (tree1 + tree2) + tree3
    tree1_copy = from_list(pairs1)
    concat(tree1_copy, tree2)
    concat(tree1_copy, tree3)
    result1 = to_list(tree1_copy)

    #  tree1 + (tree2 + tree3)
    tree2_tree3 = from_list(pairs2)
    concat(tree2_tree3, tree3)
    tree1_new = from_list(pairs1)
    concat(tree1_new, tree2_tree3)
    result2 = to_list(tree1_new)

    assert result1 == result2


@given(pairs=st.lists(key_value_pairs))
def test_monoid(pairs):
    tree = from_list(pairs)
    empty_tree = empty()

    #  tree + empty = tree
    tree_copy = from_list(pairs)
    concat(tree_copy, empty_tree)
    assert to_list(tree_copy) == to_list(tree)

    #  empty + tree = tree
    empty_copy = empty()
    concat(empty_copy, tree)
    assert to_list(empty_copy) == to_list(tree)
