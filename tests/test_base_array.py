import pytest
import vtk
from vtk.util import numpy_support as ns

from vtky.DataArray import *


@pytest.fixture
def data_array1():
    result = BaseArray(np.arange(10, dtype=np.double), np.double)
    result.SetName('test_name')
    return result

@pytest.fixture
def data_array2():
    np_array = np.arange(5, dtype=np.double)
    result = BaseArray(np_array)
    result.SetName('test_name_modified')
    return result

@pytest.fixture
def vtk_double():
    result = vtk.vtkDoubleArray()
    result.SetName('test_name_modified')
    result.InsertNextValue(0.0)
    result.InsertNextValue(1.0)
    result.InsertNextValue(2.0)
    result.InsertNextValue(3.0)
    result.InsertNextValue(4.0)
    return result


def test_compare_list(data_array2):
    list = [0., 1., 2., 3., 4.]
    assert data_array2 == list

    array = BaseArray(list)
    assert array == list

def test_set_vtk(vtk_double, data_array2, data_array1):
    array = DoubleArray()
    array.vtk = vtk_double
    assert array == vtk_double
    assert array == data_array2
    assert array != data_array1

def test_compare_dataframe(data_array2):
    import pandas as pd
    dataframe = pd.DataFrame([0., 1., 2., 3., 4.])
    assert data_array2 == dataframe

    array = BaseArray(dataframe)
    assert array == dataframe

def test_compare_with_vtk(data_array1, data_array2, vtk_double):
    assert data_array1 != vtk_double
    assert data_array2 == vtk_double


def test_data_array(data_array1, data_array2):
    assert data_array1 == data_array1
    assert data_array2 == data_array2
    assert str(data_array1) == 'test_name: [ 0.  1.  2.  3.  4.  5.  6.  7.  8.  9.]'
    assert str(data_array2) == 'test_name_modified: [ 0.  1.  2.  3.  4.]'

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
    assert str(array) == 'test_name_modified: [  0.   1.   2.   3.   4.  99.]'

    array.RemoveLastTuple()
    assert array.numpy.size == 5
    assert array[4] == 4
    assert array == [0, 1, 2, 3, 4]
    assert array == np.array([0, 1, 2, 3, 4])
    assert array.GetTuple1(4) == 4


def test_replace_values_numpy(vtk_double):
    array = BaseArray(vtk_double)
    array.numpy = np.ones(3)

    assert array == np.ones(3)
    assert array.GetTuple1(0) == 1
    assert array.GetTuple1(1) == 1
    assert array.GetTuple1(2) == 1
    assert np.array_equal(array.numpy, np.ones(3))
    assert str(array) == 'test_name_modified: [ 1.  1.  1.]'


@pytest.fixture
def vtk_3d(numpy_3d):
    vtk_array = ns.numpy_to_vtk(numpy_3d)
    vtk_array.SetName('VTK3D')
    return vtk_array

@pytest.fixture
def numpy_3d():
    return np.arange(9).reshape(-1, 3)


def test_3d_array(vtk_3d, numpy_3d):
    def _aux_test(array, name):
        array = BaseArray(array)
        array.SetName(name)
        assert array == array
        assert np.array_equal(array.numpy, numpy_3d)
        assert str(array) == 'VTK3D: [[0 1 2]\n [3 4 5]\n [6 7 8]]'

        assert array[0, 0] == 0
        assert array[0, 1] == 1
        assert array[0, 2] == 2
        assert array[1, 0] == 3
        assert array[1, 1] == 4
        assert array[1, 2] == 5
        assert array[2, 0] == 6
        assert array[2, 1] == 7
        assert array[2, 2] == 8

        assert array.GetTuple3(0) == (0, 1, 2)
        assert array.GetTuple3(1) == (3, 4, 5)
        assert array.GetTuple3(2) == (6, 7, 8)

    _aux_test(vtk_3d, vtk_3d.GetName())
    _aux_test(numpy_3d, 'VTK3D')

def test_add(data_array2):
    result = data_array2 + 10
    assert result == [10, 11, 12, 13, 14]
    assert isinstance(result, BaseArray)
    assert result == np.array([10, 11, 12, 13, 14])
    assert result.GetName() == data_array2.GetName()
    assert result.GetTuple1(0) == 10
    assert result.GetTuple1(1) == 11
    assert result.GetTuple1(2) == 12
    assert result.GetTuple1(3) == 13
    assert result.GetTuple1(4) == 14

def test_sub(data_array2):
    result = data_array2 - 10
    assert result == [-10, -9, -8, -7, -6]
    assert isinstance(result, BaseArray)
    assert result == np.array([-10, -9, -8, -7, -6])
    assert result.GetName() == data_array2.GetName()
    assert result.GetTuple1(0) == -10
    assert result.GetTuple1(1) == -9
    assert result.GetTuple1(2) == -8
    assert result.GetTuple1(3) == -7
    assert result.GetTuple1(4) == -6

def test_multiplication(data_array2):
    result = data_array2 * 10
    assert result == [0, 10, 20, 30, 40]
    assert isinstance(result, BaseArray)
    assert result == np.array([0, 10, 20, 30, 40])
    assert result.GetName() == data_array2.GetName()
    assert result.GetTuple1(0) == 0
    assert result.GetTuple1(1) == 10
    assert result.GetTuple1(2) == 20
    assert result.GetTuple1(3) == 30
    assert result.GetTuple1(4) == 40

def test_div(data_array2):
    result = data_array2 / 2.0
    assert result == [0, 0.5, 1, 1.5, 2]
    assert isinstance(result, BaseArray)
    assert result == np.array([0, 0.5, 1, 1.5, 2])
    assert result.GetName() == data_array2.GetName()
    assert result.GetTuple1(0) == 0
    assert result.GetTuple1(1) == 0.5
    assert result.GetTuple1(2) == 1
    assert result.GetTuple1(3) == 1.5
    assert result.GetTuple1(4) == 2
