import numpy as np
import pytest
import vtk

from vtky.Points import Points


@pytest.fixture
def vtk_points():
    points = vtk.vtkPoints()
    points.InsertNextPoint(0., 1., 2.)
    points.InsertNextPoint(1., 2., 3.)
    points.InsertNextPoint(2., 3., 4.)
    return points

@pytest.fixture
def np_points():
    points = np.array([[0., 1., 2.],
                       [1., 2., 3.],
                       [2., 3., 4.]])
    return points

def test_create_points(vtk_points, np_points):
    points = Points(vtk_points)
    assert points == vtk_points
    assert points == np_points

    points = Points(np_points)
    assert points == vtk_points
    assert points == np_points