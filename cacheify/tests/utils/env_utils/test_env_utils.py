import os
import pytest
from cacheify.utils import get_env_var

def test_get_env_var_int():
    os.environ['TEST_INT'] = '42'
    result = get_env_var('TEST_INT', var_type=int)
    assert result == 42
    assert isinstance(result, int)

def test_get_env_var_float():
    os.environ['TEST_FLOAT'] = '3.14'
    result = get_env_var('TEST_FLOAT', var_type=float)
    assert result == 3.14
    assert isinstance(result, float)

def test_get_env_var_bool_true():
    os.environ['TEST_BOOL'] = 'true'
    result = get_env_var('TEST_BOOL', var_type=bool)
    assert result is True
    assert isinstance(result, bool)

def test_get_env_var_bool_false():
    os.environ['TEST_BOOL'] = 'false'
    result = get_env_var('TEST_BOOL', var_type=bool)
    assert result is False
    assert isinstance(result, bool)

def test_get_env_var_bool_numeric():
    os.environ['TEST_BOOL'] = '1'
    result = get_env_var('TEST_BOOL', var_type=bool)
    assert result is True

    os.environ['TEST_BOOL'] = '0'
    result = get_env_var('TEST_BOOL', var_type=bool)
    assert result is False

def test_get_env_var_string():
    os.environ['TEST_STRING'] = 'Hello World'
    result = get_env_var('TEST_STRING', var_type=str)
    assert result == 'Hello World'
    assert isinstance(result, str)

def test_get_env_var_default_value():
    result = get_env_var('NON_EXISTENT_VAR', default='default_value')
    assert result == 'default_value'
    assert isinstance(result, str)

def test_get_env_var_invalid_int():
    os.environ['TEST_INVALID_INT'] = 'invalid'
    result = get_env_var('TEST_INVALID_INT', default=0, var_type=int)
    assert result == 0

def test_get_env_var_invalid_float():
    os.environ['TEST_INVALID_FLOAT'] = 'invalid'
    result = get_env_var('TEST_INVALID_FLOAT', default=0.0, var_type=float)
    assert result == 0.0

def test_get_env_var_invalid_bool():
    os.environ['TEST_INVALID_BOOL'] = 'notabool'
    result = get_env_var('TEST_INVALID_BOOL', default=False, var_type=bool)
    assert result is False
