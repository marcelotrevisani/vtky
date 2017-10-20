import numpy as np
import pandas as pd
from vtk.util import numpy_support as ns


class BaseArray(object):

    def __init__(self, np_array):
        type = ns.get_vtk_array_type(np_array)
        self._vtk = ns.create_vtk_array(type)

        if isinstance(np_array, list):
            np_array = np.array(np_array)
        elif isinstance(np_array, pd.DataFrame):
            np_array = np_array.as_matrix()

        if isinstance(np_array, np.ndarray):
            self._set_data_array(np_array)
        else:
            raise ValueError('Expected a Numpy array, but received a: {}'.format(type(np_array)))

    def __getattr__(self, item):
        try:
            return getattr(self._vtk, item)
        except AttributeError, msg:
            raise AttributeError('Object has not attribute {}'.format(msg.message))

    def __eq__(self, other):
        if isinstance(other, np.ndarray):
            return np.array_equal(self._numpy, other)
        if isinstance(other, type(self)) and not np.array_equal(self._numpy, ns.vtk_to_numpy(other)):
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
        if self._numpy.size == 0:
            self._numpy = row_val
        else:
            self._numpy = np.vstack((self._numpy, row_val))

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
        self._set_data_array(array)
