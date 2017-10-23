import pytest
import numpy as np

from vtky.BaseArray import BaseArray

@pytest.fixture
def data_array1():
    result = BaseArray(np.arange(10, dtype='d'))
    result.SetName('test_name')
    return result

@pytest.fixture
def data_array2():
    np_array = np.arange(10, dtype='d')
    result = BaseArray(np_array)
    result.SetName('test_name_modified')
    return result

def test_data_array(data_array1, data_array2):
    assert data_array1 == data_array1
    assert data_array2 == data_array2

    assert data_array1 != data_array2

    assert data_array1[0] == data_array1.GetTuple1(0)
    assert data_array1[0] == 0
    assert data_array1.GetTuple1(0) == 0

    assert data_array1[9] == data_array1.GetTuple1(9)
    assert data_array1[9] == 9
    assert data_array1.GetTuple1(9) == 9

    data_array1[9] = 10
    assert data_array1[9] == data_array1.GetTuple1(9)
    assert data_array1[9] == 10
    assert data_array1.GetTuple1(9) == 10




