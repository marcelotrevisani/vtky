import pytest
import numpy as np

from vtky.baseArray import BaseArray

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



