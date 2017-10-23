import numpy as np
import pandas as pd
import six
from vtk.util import numpy_support as ns


class BaseArray(object):

    def __init__(self, np_array, type=None):
        if isinstance(np_array, list):
            np_array = np.array(np_array)
        elif isinstance(np_array, pd.DataFrame):
            np_array = np_array.as_matrix()

        if isinstance(np_array, np.ndarray):
            if type:
                np_array = np_array.astype(type)
            vtk_type = ns.get_vtk_array_type(np_array.dtype)
            self._vtk = ns.create_vtk_array(vtk_type)
            self._set_data_array(np_array)
        else:
            raise ValueError('Expected a Numpy array, but received a: {}'.format(type(np_array)))


    def __getattr__(self, item):
        if isinstance(item, six.string_types) and item == 'array':
            return self._numpy
        else:
            try:
                return getattr(self._vtk, item)
            except AttributeError as msg:
                raise AttributeError('Object has not attribute {}'.format(msg.message))

    def __eq__(self, other):
        if isinstance(other, np.ndarray):
            return np.array_equal(self._numpy, other)
        if isinstance(other, type(self)) and not np.array_equal(self._numpy, other.array):
            return False
        return self.GetNumberOfComponents() == other.GetNumberOfComponents() and \
               self.GetNumberOfTuples() == other.GetNumberOfTuples() and \
               self._numpy.size == other.GetNumberOfTuples() and \
               self.GetName() == other.GetName()

    def __contains__(self, item):
        return item in self._numpy

    def __len__(self):
        return self._numpy.size

    def __getitem__(self, index):
        cls = type(self)

        if isinstance(index, slice):
            return cls(self._numpy[index])
        else:
            return self._numpy[index]

    def __setitem__(self, key, value):
        self._numpy[key] = value

    def add_row(self, row_val):
        '''
        Receives a new row which will be add to the vtkDataArray
        :param row_val: Receives a numpy array or a list to be add
        '''
        if self._numpy.size == 0:
            self._numpy = row_val
        else:
            self._numpy = np.vstack((self._numpy, row_val))
            self._set_data_array(self._numpy)

    def _set_data_array(self, array):
        '''
        Receives a numpy array and set it to a private attribute
        :param array: numpy array
        '''
        if not array.flags.contiguous:
            array = np.ascontiguousarray(array)

        if len(array.shape) == 1:
            self.SetNumberOfComponents(1)
        else:
            self.SetNumberOfComponents(array.shape[1])

        self.SetNumberOfTuples(array.shape[0])
        data_flat = np.ravel(array)
        self._numpy = data_flat
        self.SetVoidArray(data_flat, len(data_flat), 1)

    def copy_array(self, array):
        '''
        Set the data to the vtkDataArray
        :param array: receives a pandas DataFrame, numpy array or a list
        :return:
        '''
        self._set_data_array(array)

