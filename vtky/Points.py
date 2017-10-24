import numpy as np
import pandas as pd
import six
import vtk

from vtky.BaseArray import BaseArray


class Points(object):

    def __init__(self, array, array_name='point_values'):
        if isinstance(array, list):
            array = np.array(array)
        elif isinstance(array, pd.DataFrame):
            array = array.as_matrix()

        if isinstance(array, vtk.vtkPoints):
            self._vtk = array
            self._points = BaseArray(array.GetData())
        elif isinstance(array, np.ndarray):
            shape = array.shape
            if len(shape) != 2:
                raise ValueError('Expected a numpy array with 2 or 3 columns, received 1')
            if len(shape) == 2 and shape[1] == 2:
                array = np.column_stack((array, np.zeros(array.shape[0])))
            elif len(shape) == 2 and (shape[1] < 2 or shape[1] > 3):
                raise ValueError('Expected a numpy array with 2 or 3 columns, received: {}'.format(shape[1]))

            self._points = BaseArray(array)
            self._vtk = vtk.vtkPoints()
            self._vtk.SetData(self._points.vtk)
            self._points.SetName(array_name)
            self._points = self._points.numpy.reshape(-1, 3)
        else:
            raise ValueError('Expected a Numpy array, but received a: {}'.format(type(array)))

    def __eq__(self, other):
        if isinstance(other, vtk.vtkPoints):
            return self._points == other.GetData()
        return self._points == other

    @property
    def x(self):
        return self._points.numpy[:, 0]

    @x.setter
    def x(self, value):
        self._points.numpy[:, 0] = value

    @property
    def y(self):
        return self._points.numpy[:, 1]

    @y.setter
    def y(self, value):
        self._points.numpy[:, 1] = value

    @property
    def z(self):
        return self._points.numpy[:, 2]

    @z.setter
    def z(self, value):
        self._points.numpy[:, 2] = value

    @property
    def xyz(self):
        return self._points

    @xyz.setter
    def xyz(self, value):
        self._points = value

    def __getattr__(self, item):
        try:
            return getattr(self._vtk, item)
        except AttributeError as msg:
            raise AttributeError('Object has not attribute {}'.format(msg.message))

    def add_row(self, points):
        pass