import pytest
import numpy as np

from vtky.baseArray import BaseArray

@pytest.fixture
def data_array():
    result = BaseArray(np.arange(10, dtype='d'))
    result.SetName('test_name')
    return result

def test_copy_array(data_array):
    data_array.copy_array(np.array([10, 11, 12, 13]))

    print('teste')
