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
            self.vtk.SetName(array_name)
        else:
            raise ValueError('Expected a Numpy array, but received a: {}'.format(type(array)))

    def __eq__(self, other):
        return self._points == other

    def __getattr__(self, item):
        if isinstance(item, six.string_types) and item == 'x':
            return self._points[:, 0]
        elif isinstance(item, six.string_types) and item == 'y':
            return self._points[:, 1]
        elif isinstance(item, six.string_types) and item == 'z' and self._points.shape[1] == 3:
            return self._points[:, 2]
        elif isinstance(item, six.string_types) and item == 'xyz':
            return self._points
        try:
            return getattr(self._vtk_points, item)
        except AttributeError as msg:
            raise AttributeError('Object has not attribute {}'.format(msg.message))

    def add_row(self, points):
        pass