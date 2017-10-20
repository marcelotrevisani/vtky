import numpy as np
import vtk
from vtk.util import numpy_support as ns
import numbers

class DoubleArray(vtk.vtkDoubleArray):

    def __init__(self, data=None):
        if data is None:
            super(DoubleArray, self).__init__()
            self._data = ns.vtk_to_numpy(self)
        elif isinstance(data, np.ndarray):
            self._set_data_array(data)
        else:
            raise ValueError('Expected a vtk.vtkDataArray or a numpy array, '
                             'but received a: {}'.format(type(data)))

    def __eq__(self, other):
        if isinstance(other, np.ndarray):
            return np.array_equal(self._data, other)
        if isinstance(other, DoubleArray) and not np.array_equal(self._data, other._data):
            return False
        if isinstance(other, vtk.vtkDoubleArray) and not np.array_equal(self._data, ns.vtk_to_numpy(other)):
            return False
        return self.GetNumberOfComponents() == other.GetNumberOfComponents() and \
               self.GetNumberOfTuples() == other.GetNumberOfTuples() and \
               self._data.size == other.GetNumberOfTuples() and \
               self.GetName() == other.GetName()


    def __contains__(self, item):
        return item in self._data

    def __len__(self):
        return self._data.size

    def __getitem__(self, index):
        cls = type(self)

        if isinstance(index, slice):
            return cls(self._data[index])
        else:
            return self._data[index]


    def __setitem__(self, key, value):
        pass


    def add_row(self, row_val):
        if self._data.size == 0:
            self._data = row_val
        else:
            self._data = np.vstack((self._data, row_val))


    def _set_data_array(self, data):
        data = data.astype('d')
        self._data = data
        if len(data.shape) == 1:
            self.SetNumberOfComponents(1)
        else:
            self.SetNumberOfComponents(data.shape[1])
        self.SetNumberOfTuples(data.shape[0])
        data_flat = np.ravel(data)
        self.SetVoidArray(data_flat, len(data_flat), 1)


    def copy_array(self, array):
        self._set_data_array(array)
