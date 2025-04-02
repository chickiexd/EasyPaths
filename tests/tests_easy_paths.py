import pytest

from easypaths import EasyPaths


def test_init():
    pm = EasyPaths()
    assert pm.project_dir is None
    assert pm.user_paths == {}
    with pytest.raises(ValueError) as excinfo:
        pm.set_current_user("chickie")
    assert str(excinfo.value) == "EasyEasyPaths is not initialized with a project dir."
    with pytest.raises(ValueError) as excinfo:
        pm.get_path("asdfga")
    assert str(excinfo.value) == "EasyEasyPaths is not initialized with a project dir."
    with pytest.raises(ValueError) as excinfo:
        pm.add_path("alkddsjg", "alksdjglka")
    assert str(excinfo.value) == "EasyEasyPaths is not initialized with a project dir."

    pm = EasyPaths("EasyPaths")
    assert list(pm.user_paths.keys()) == ["test", "chickie"]
    assert pm.current_user is None


def test_set_current_user():
    # with valid project_dir
    pm = EasyPaths("EasyPaths")
    pm.set_current_user("chickie")
    assert pm.current_user == "chickie"
    assert pm.get_path("project_dir") == "/home/chickie/personal/coding/EasyPaths/"

    # without valid project_dir
    pm = EasyPaths("EasyPaths")
    with pytest.raises(ValueError) as excinfo:
        pm.set_current_user("test")
    assert str(excinfo.value) == "Users project directory does not exist."

    # without valid user
    pm = EasyPaths("EasyPaths")
    with pytest.raises(ValueError) as excinfo:
        pm.set_current_user("test2")
    assert str(excinfo.value) == "User does not exist."


def test_project_dir():
    pm = EasyPaths("EasyPaths")
    pm.set_current_user("chickie")
    assert pm.get_path("project_dir") == "/home/chickie/personal/coding/EasyPaths"

    pm = EasyPaths("/EasyPaths/")
    pm.set_current_user("chickie")
    assert pm.get_path("project_dir") == "/home/chickie/personal/coding/EasyPaths"

    pm = EasyPaths("/EasyPaths")
    pm.set_current_user("chickie")
    assert pm.get_path("project_dir") == "/home/chickie/personal/coding/EasyPaths"

    pm = EasyPaths("EasyPaths/")
    pm.set_current_user("chickie")
    assert pm.get_path("project_dir") == "/home/chickie/personal/coding/EasyPaths"


def test_add_user():
    pm = EasyPaths("EasyPaths")
    pm.add_user("test2", "/home/chickie/personal/coding/test2")
    assert "test2" in pm.user_paths
    path = pm.get_path("project_dir", "test2")
    assert path == "/home/chickie/personal/coding/test2/EasyPaths"


def test_add_path():
    pm = EasyPaths("EasyPaths")
    pm.add_user("test2", "/home/chickie/personal/coding/test2")

    pm.add_path("data", "data", False, "test2")
    path = pm.get_path("data", "test2")
    assert path == "/home/chickie/personal/coding/test2/EasyPaths/data"

    pm.add_path("data", "data/", False, "test2")
    path = pm.get_path("data", "test2")
    assert path == "/home/chickie/personal/coding/test2/EasyPaths/data"

    with pytest.raises(ValueError) as excinfo:
        pm.add_path("data", "/data", False, "test2")
    assert (
        str(excinfo.value)
        == "Path value must be a relative path. Please use add_abs_path instead or remove leading /"
    )

    with pytest.raises(ValueError) as excinfo:
        pm.add_path("data", "", False, "test2")
    assert str(excinfo.value) == "Path value cannot be empty."

    pm.add_path("", "data/", False, "test2")
    path = pm.get_path("", "test2")
    assert path == "/home/chickie/personal/coding/test2/EasyPaths/data"

    with pytest.raises(ValueError) as excinfo:
        pm.add_path("data", "data", False, "alksglka")
    assert str(excinfo.value) == "User does not exist. Please add the user first."

    pm.add_path("data", "data")
    path = pm.get_path("data", "test2")
    assert path == "/home/chickie/personal/coding/test2/EasyPaths/data"
    path = pm.get_path("data", "chickie")
    assert path == "/home/chickie/personal/coding/EasyPaths/data"


def test_add_abs_path():
    pm = EasyPaths("EasyPaths")
    pm.add_user("test2", "/home/chickie/personal/coding/test2")

    with pytest.raises(ValueError) as excinfo:
        pm.add_abs_path("data", "data", "test2")
    assert str(excinfo.value) == "Path value must be an absolute path."

    pm.add_abs_path("data", "/data", "test2")
    path = pm.get_path("data", "test2")
    assert path == "/data"

    pm.add_abs_path("", "/data", "test2")
    path = pm.get_path("", "test2")
    assert path == "/data"

    with pytest.raises(ValueError) as excinfo:
        pm.add_abs_path("data", "/data", "alksglka")
    assert str(excinfo.value) == "User does not exist. Please add the user first."

    pm.add_abs_path("data", "/data")
    path = pm.get_path("data", "test2")
    assert path == "/data"
    path = pm.get_path("data", "chickie")
    assert path == "/data"


def test_get_path():
    pm = EasyPaths("EasyPaths")
    pm.set_current_user("chickie")

    assert pm.get_path("project_dir") == "/home/chickie/personal/coding/EasyPaths"
    assert (
        pm.get_path("project_dir", "chickie")
        == "/home/chickie/personal/coding/EasyPaths"
    )

    with pytest.raises(ValueError) as excinfo:
        pm.get_path("project_dir", "laksjglka")
    assert str(excinfo.value) == "User does not exist. Please add the user first."

    with pytest.raises(ValueError) as excinfo:
        pm.get_path("alkshdfglah", "chickie")
    assert str(excinfo.value) == "Path key not found for user."

    pm = EasyPaths("EasyPaths")
    with pytest.raises(ValueError) as excinfo:
        pm.get_path("alkshdfglah")
    assert (
        str(excinfo.value)
        == "No user set. Please set a user first or provide a user_id."
    )
