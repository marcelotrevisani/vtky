import pytest
import vtk

from vtky.DataArray import *


@pytest.fixture(params=[
    (DoubleArray(), vtk.vtkDoubleArray),
    (FloatArray(),vtk.vtkFloatArray),
    (IntArray(), vtk.vtkIntArray),
    (UnsignedCharArray(), vtk.vtkUnsignedCharArray),
    (IdTypeArray(), vtk.vtkIdTypeArray),
    (LongArray(), vtk.vtkLongArray),
    (LongLongArray(), vtk.vtkLongLongArray),
    (ShortArray(), vtk.vtkShortArray),
    (UnsignedIntArray(), vtk.vtkUnsignedIntArray),
    (UnsignedLongArray(), vtk.vtkUnsignedLongArray),
    (UnsignedLongLongArray(), vtk.vtkUnsignedLongLongArray),
    (UnsignedShortArray(), vtk.vtkUnsignedShortArray),
])
def data_array(request):
    array = request.param
    return array

def test_data_array_objects(data_array):
    assert isinstance(data_array[0].vtk, data_array[1])