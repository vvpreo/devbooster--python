from devbooster.common import get_project_root


def test_project_root():
    root  = get_project_root("poetry.lock")
    print(root)