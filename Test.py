from hypothesis import given, strategies as st
import Binary_tree
import pytest

BSTDictionary = Binary_tree.BSTDictionary
bst_strategy = st.builds(BSTDictionary)

keys_strategy = st.integers(min_value=0, max_value=100)
values_strategy = st.text(min_size=1, max_size=10)

@given(bst=bst_strategy, key=keys_strategy, value=values_strategy)
def test_add_and_search(bst, key, value):
    bst.add(key, value)
    assert bst.search(key) == value

@given(bst=bst_strategy, key=keys_strategy, value=values_strategy, new_value=values_strategy)
def test_update(bst, key, value, new_value):
    bst.add(key, value)
    bst.update(key, new_value)
    assert bst.search(key) == new_value

@given(bst=bst_strategy, key=keys_strategy, value=values_strategy)
def test_delete(bst, key, value):
    bst.add(key, value)
    bst.delete(key)
    assert bst.search(key) is None

if __name__ == "__main__":
    pytest.main()