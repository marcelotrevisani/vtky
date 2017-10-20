import pytest
import numpy as np

from vtky.doubleArray import DoubleArray

@pytest.fixture
def data_array():
    result = DoubleArray(np.arange(10))
    result.SetName('test_name')
    return result

def test_copy_array(data_array):
    data_array.copy_array(np.array([10, 11, 12, 13]))

    print('teste')
