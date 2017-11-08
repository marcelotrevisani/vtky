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

@pytest.fixture
def points(np_points):
    return Points(np_points)

def test_create_points(vtk_points, np_points):
    points = Points(vtk_points)
    assert points == vtk_points
    assert points == np_points

    points = Points(np_points)
    assert points == vtk_points
    assert points == np_points

def test_compare_points(points, np_points):
    points2 = Points(np_points)
    assert points == points2

def test_xyz_points(points, np_points):
    assert np.array_equal(points.x, np_points[:, 0])
    assert np.array_equal(points.y, np_points[:, 1])
    assert np.array_equal(points.z, np_points[:, 2])
    assert np.array_equal(points.xyz, np_points)

def test_change_xyz(points):
    points.xyz = np.ones(12).reshape(-1, 3)
    assert points == np.ones(12).reshape(-1, 3)
    assert points.GetPoint(0) == (1, 1, 1)
    assert points.GetPoint(1) == (1, 1, 1)
    assert points.GetPoint(2) == (1, 1, 1)
    assert points.GetPoint(3) == (1, 1, 1)

    points.x = np.zeros(4)
    points.y = np.ones(4)
    points.z = np.full(4, 2, dtype=np.double)
    np_expected = np.array([[0, 1, 2],
                            [0, 1, 2],
                            [0, 1, 2],
                            [0, 1, 2]])
    assert points == np_expected
    assert points.GetPoint(0) == (0, 1, 2)
    assert points.GetPoint(1) == (0, 1, 2)
    assert points.GetPoint(2) == (0, 1, 2)
    assert points.GetPoint(3) == (0, 1, 2)

    points.xyz = np.full((5, 3), 11, dtype=np.double)
    np_expected = np.full((5, 3), 11, dtype=np.double)
    assert np.array_equal(points.xyz, np_expected)
    assert points == np_expected
    assert points.GetPoint(0) == (11, 11, 11)
    assert points.GetPoint(1) == (11, 11, 11)
    assert points.GetPoint(2) == (11, 11, 11)
    assert points.GetPoint(3) == (11, 11, 11)
    assert points.GetPoint(4) == (11, 11, 11)


def test_add_row(points):
    points.add_row([10, 11, 12])
    assert np.array_equal(points[-1, :], [10, 11, 12])
    assert points.GetPoint(0) == (0, 1, 2)
    assert points.GetPoint(1) == (1, 2, 3)
    assert points.GetPoint(2) == (2, 3, 4)
    assert points.GetPoint(3) == (10, 11, 12)

def test_add_points_vtk(np_points):
    points = Points(np_points)
    points.InsertNextPoint(9, 9, 9)
    np_expected = np.array([[0., 1., 2.],
                            [1., 2., 3.],
                            [2., 3., 4.],
                            [9., 9., 9.]])

    assert points == np_expected
    assert np.array_equal(points.x, [0, 1, 2, 9])
    assert np.array_equal(points.y, [1, 2, 3, 9])
    assert np.array_equal(points.z, [2, 3, 4, 9])
    assert np.array_equal(points.xyz, np_expected)
    assert points.GetPoint(0) == (0, 1, 2)
    assert points.GetPoint(1) == (1, 2, 3)
    assert points.GetPoint(2) == (2, 3, 4)
    assert points.GetPoint(3) == (9, 9, 9)

def test_add(points, np_points):
    np_points = np_points + 10
    points = points + 10
    assert points == np_points
    assert points.GetPoint(0) == (10, 11, 12)
    assert points.GetPoint(1) == (11, 12, 13)
    assert points.GetPoint(2) == (12, 13, 14)

def test_sub(points, np_points):
    np_points = np_points - 1
    points = points - 1
    assert points == np_points
    assert points.GetPoint(0) == (-1, 0, 1)
    assert points.GetPoint(1) == (0, 1, 2)
    assert points.GetPoint(2) == (1, 2, 3)

def test_mult(points, np_points):
    np_points = np_points * 10
    points = points * 10
    assert points == np_points
    assert points.GetPoint(0) == (0, 10, 20)
    assert points.GetPoint(1) == (10, 20, 30)
    assert points.GetPoint(2) == (20, 30, 40)

def test_div(points, np_points):
    np_points = np_points / 10
    points = points / 10
    assert points == np_points
    assert points.GetPoint(0) == (.0, .1, .2)
    assert points.GetPoint(1) == (.1, .2, .3)
    assert points.GetPoint(2) == (.2, .3, .4)
