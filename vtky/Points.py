import numpy as np
import pandas as pd
import vtk

from vtky.BaseArray import BaseArray


class Points(object):

    def __init__(self, array, array_name='Points'):
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
        else:
            raise ValueError('Expected a Numpy array, but received a: {}'.format(type(array)))

    def __eq__(self, other):
        if isinstance(other, vtk.vtkPoints):
            return self._points == other.GetData()
        return self._points == other

    def _check_size_column(self, array):
        if len(array.shape) != 1:
            raise ValueError('Expected an flat array, got an array with {} columns'.format(array.shape[1]))
        if array.size != self.x.size:
            raise ValueError('Expected an array with the size {}, got {}'.format(self.x.size, array.size))

    @property
    def x(self):
        return self._points.numpy[:, 0]

    @x.setter
    def x(self, value):
        value = np.array(value)
        self._check_size_column(value)
        self._points.numpy[:, 0] = value

    @property
    def y(self):
        return self._points.numpy[:, 1]

    @y.setter
    def y(self, value):
        value = np.array(value)
        self._check_size_column(value)
        self._points.numpy[:, 1] = value

    @property
    def z(self):
        return self._points.numpy[:, 2]

    @z.setter
    def z(self, value):
        value = np.array(value)
        self._check_size_column(value)
        self._points.numpy[:, 2] = value

    @property
    def xyz(self):
        return self._points.numpy

    @xyz.setter
    def xyz(self, value):
        self._points.numpy = value

    def __getattr__(self, item):
        try:
            attr = getattr(self._vtk, item)
            if hasattr(attr, "__self__") and attr.__self__ is self._vtk:
                def _vtk_method_proxy(*args, **kwargs):
                    '''
                    This is black magic, do not do this at home. :)
                    It is need because the self._vtk.AddObserver(vtk.vtkCommand.ModifiedEvent, update_numpy)
                    only works if the method Modified() is called, when we add a value or remove it, it will not
                    be called.
                    :param args:
                    :param kwargs:
                    :return:
                    '''
                    result = attr(*args, **kwargs)
                    self._points.Modified()
                    return result

                return _vtk_method_proxy
            else:
                return attr
        except AttributeError as msg:
            raise AttributeError('Object has not attribute {}'.format(msg.message))

    def __getitem__(self, index):
        return self._points[index]

    def add_row(self, points):
        '''
        Add a new row into the the vtk array. Expected a numpy array or a list with x, y and z. If passa just
        two columns the code will consider the z value as zero.
        :param points: list or numpy array
        '''
        if isinstance(points, list):
            points = np.array(points)
        if len(points.shape) == 1:
            if points.shape[0] == 2:
                points = np.append(points, 0)
            if points.shape[0] != 3:
                raise ValueError('Expected an array with 3 or 2 columns, received: {}'.format(points.shape[0]))
        else:
            if points.shape[1] == 2:
                points = points.column_stack((points, np.zeros(points.shape[0])))
            if points.shape[1] != 3:
                raise ValueError('Expected an array with 3 or 2 columns, received: {}'.format(points.shape[1]))
        self.xyz = np.vstack((self.xyz, points))
