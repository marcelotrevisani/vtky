import numpy as np
import vtk
from vtk.util import numpy_support as ns
import numbers

class DoubleArray(vtk.vtkDoubleArray):


    def add_row(self, row_val):
        if self._data.size == 0:
            self._data = row_val
        else:
            self._data = np.vstack((self._data, row_val))

    def __eq__(self, other):
        pass

    def __getitem__(self, index):
        cls = type(self)

        if isinstance(index, slice):
            return cls(self._data[index])
        else:
            return self._data[index]


    def __setitem__(self, key, value):
        pass

    def __init__(self, data=None):
        if data is None:
            super(DoubleArray, self).__init__()
            self._data = ns.vtk_to_numpy(self)
        elif isinstance(data, np.ndarray):
            self._set_data_array(data)
        else:
            raise ValueError('Expected a vtk.vtkDataArray or a numpy array, '
                             'but received a: {}'.format(type(data)))

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
