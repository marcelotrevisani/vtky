import numpy as np
import vtk
from vtk.util import numpy_support as ns

class DataArray(vtk.vtkDataArray):

    def add_column(self, col_val):
        '''

        :param col_val:
        :return:
        '''
        if self._data.size == 0:
            self._data = col_val
        else:
            self._data = np.column_stack((self._data, col_val))

    def add_row(self, row_val):
        if self._data.size == 0:
            self._data = row_val
        else:
            self._data = np.vstack((self._data, row_val))

    def __eq__(self, other):
        pass

    def __getitem__(self, item):
        return self._data.item(item)

    def __setitem__(self, key, value):
        pass

    def __init__(self):
        super(DataArray, self).__init__()
        self._data = ns.vtk_to_numpy(self)

    def copy_vtk(self, vtk_data):
        self = vtk_data
        self._data = ns.vtk_to_numpy(vtk_data)
