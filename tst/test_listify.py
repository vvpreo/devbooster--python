import pytest

from devbooster.common import listify


@pytest.mark.parametrize("arg", [1, "a", ["somelist"]])
def test_listify(arg):
    l_a = listify(arg)
    assert l_a == [arg] if not isinstance(arg, list) else arg
