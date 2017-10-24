import pytest
import vtk

from vtky.DataArray import *

@pytest.fixture
def data_array1():
    result = BaseArray(np.arange(10, dtype='d'))
    result.SetName('test_name')
    return result

@pytest.fixture
def data_array2():
    np_array = np.arange(5, dtype='d')
    result = BaseArray(np_array)
    result.SetName('test_name_modified')
    return result

@pytest.fixture
def vtk_double():
    result = vtk.vtkDoubleArray()
    result.SetName('test_name_modified')
    result.InsertNextValue(0)
    result.InsertNextValue(1)
    result.InsertNextValue(2)
    result.InsertNextValue(3)
    result.InsertNextValue(4)
    return result

def test_compare_with_vtk(data_array1, data_array2, vtk_double):
    assert data_array1 != vtk_double
    assert data_array2 == vtk_double


def test_data_array(data_array1, data_array2):
    assert data_array1 == data_array1
    assert data_array2 == data_array2
    assert str(data_array1) == 'test_name\n[ 0.  1.  2.  3.  4.  5.  6.  7.  8.  9.]'
    assert str(data_array2) == 'test_name_modified\n[ 0.  1.  2.  3.  4.]'

    assert data_array1 == np.arange(10)
    assert data_array2 == np.arange(5)
    assert np.array_equal(data_array1.numpy, np.arange(10))
    assert np.array_equal(data_array2.numpy, np.arange(5))

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

    data_array1.SetTuple1(9, 11)
    assert data_array1[9] == data_array1.GetTuple1(9)
    assert data_array1[9] == 11
    assert data_array1.GetTuple1(9) == 11


def test_data_array_slice(data_array1):
    sl = data_array1[2:4]
    assert sl[0] == data_array1[2]
    assert sl[0] == data_array1.GetTuple1(2)
    assert sl[1] == data_array1[3]
    assert sl[1] == data_array1.GetTuple1(3)

    sl = data_array1[:4]
    assert sl[0] == data_array1[0]
    assert sl[1] == data_array1[1]
    assert sl[2] == data_array1[2]
    assert sl[3] == data_array1[3]
    assert sl[0] == data_array1.GetTuple1(0)
    assert sl[1] == data_array1.GetTuple1(1)
    assert sl[2] == data_array1.GetTuple1(2)
    assert sl[3] == data_array1.GetTuple1(3)

    sl = data_array1[::2]
    assert sl[0] == data_array1[0]
    assert sl[1] == data_array1[2]
    assert sl[2] == data_array1[4]
    assert sl[3] == data_array1[6]
    assert sl[4] == data_array1[8]
    assert sl[0] == data_array1.GetTuple1(0)
    assert sl[1] == data_array1.GetTuple1(2)
    assert sl[2] == data_array1.GetTuple1(4)
    assert sl[3] == data_array1.GetTuple1(6)
    assert sl[4] == data_array1.GetTuple1(8)


def test_create_basearray_vtk(vtk_double, data_array2):
    base_array = BaseArray(vtk_double)
    assert data_array2 == base_array
    assert str(data_array2) == str(base_array)
    assert data_array2.GetName() == base_array.GetName()

    assert vtk_double.GetTuple1(0) == base_array[0]


def test_insert_remove_values_vtk(vtk_double):
    array = BaseArray(vtk_double)
    array.InsertNextValue(99)
    assert array.GetTuple1(5) == 99
    assert array.numpy.size == 6
    assert array[5] == 99
    assert array == np.array([0, 1, 2, 3, 4, 99])
    assert array == [0, 1, 2, 3, 4, 99]

    array.RemoveLastTuple()
    assert array.numpy.size == 5
    assert array[4] == 4
    assert array == [0, 1, 2, 3, 4]
    assert array == np.array([0, 1, 2, 3, 4])
    assert array.GetTuple1(4) == 4
