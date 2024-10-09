import pytest
import sys
from cacheify.utils import python_version, compare_python_version

def test_py_version():
    version = python_version()
    assert isinstance(version, str)
    assert version.count('.') == 2
    major, minor, micro = version.split('.')
    assert major.isdigit()
    assert minor.isdigit()
    assert micro.isdigit()

@pytest.mark.parametrize("passed_version, expected", [
    ("3.9.2", -1 if sys.version_info < (3, 9, 2) else (0 if sys.version_info == (3, 9, 2) else 1)),
    ("3.9", -1 if sys.version_info < (3, 9, 0) else (0 if sys.version_info == (3, 9, 0) else 1)),
    ("3.10.1", -1 if sys.version_info < (3, 10, 1) else (0 if sys.version_info == (3, 10, 1) else 1)),
    ("2.7", 1 if sys.version_info >= (3, 0, 0) else -1),
    ("3.8.5", -1 if sys.version_info < (3, 8, 5) else (0 if sys.version_info == (3, 8, 5) else 1)),
])
def test_compare_py_version(passed_version, expected):
    assert compare_python_version(passed_version) == expected

def test_compare_py_version_invalid_format():
    with pytest.raises(ValueError, match="Invalid version format. Please use a format like '3.9.2' or '3.9'."):
        compare_python_version("invalid_version")