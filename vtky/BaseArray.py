from inspect import ismethod

import numpy as np
import pandas as pd
import vtk
from vtk.util import numpy_support as ns


class BaseArray(object):

    def __init__(self, array, type=None):
        if isinstance(array, list):
            array = np.array(array)
        elif isinstance(array, pd.DataFrame):
            array = array.as_matrix()

        if isinstance(array, np.ndarray):
            if not array.flags.contiguous:
                array = np.ascontiguousarray(array)
            if type:
                array = array.astype(type)
            self._numpy = array
            self._vtk = ns.numpy_to_vtk(self._numpy)
            self._vtk._np = array
        elif isinstance(array, vtk.vtkDataArray):
            if type is None or array.GetDataType() == ns.get_vtk_array_type(type):
                self._vtk = array
                self._numpy = ns.vtk_to_numpy(array)
            else:
                if type is None:
                    type = np.double
                np_array = ns.vtk_to_numpy(array).astype(type)
                self._vtk = ns.create_vtk_array(ns.get_vtk_array_type(np_array))
                self._vtk.SetName(array.GetName())
                self._set_data_array(np_array)
        else:
            raise ValueError('Expected a Numpy array, but received a: {}'.format(type(array)))
        self._vtk.AddObserver(vtk.vtkCommand.ModifiedEvent, self._update_numpy)

    @property
    def numpy(self):
        return self._numpy

    @numpy.setter
    def numpy(self, np_array):
        self._numpy = np_array
        self._set_data_array(np_array)

    @property
    def vtk(self):
        return self._vtk

    @vtk.setter
    def vtk(self, vtk_object):
        self._vtk = vtk_object
        array = ns.vtk_to_numpy(self._vtk)
        self._set_data_array(array)

    def __getattr__(self, item):
        try:
            return getattr(self._vtk, item)
        except AttributeError as msg:
            raise AttributeError('Object has not attribute {}'.format(msg.message))

    def __eq__(self, other):
        if isinstance(other, np.ndarray):
            return np.array_equal(self._numpy, other)
        condition = True
        if isinstance(other, BaseArray):
            condition = self._numpy.shape == other._numpy.shape
        return self.GetNumberOfComponents() == other.GetNumberOfComponents() and \
               self.GetNumberOfTuples() == other.GetNumberOfTuples() and \
               condition and self.GetName() == other.GetName()

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

    def __str__(self):
        return '{}\n{}'.format(self.GetName(), self._numpy)

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
        self.SetVoidArray(self._numpy, len(data_flat), 1)

    def _update_numpy(self, *args, **kwargs):
        # array = ns.vtk_to_numpy(self._vtk)
        # self._vtk
        self._set_data_array(ns.vtk_to_numpy(self._vtk))


    def copy_array(self, array):
        '''
        Set the data to the vtkDataArray
        :param array: receives a pandas DataFrame, numpy array or a list
        :return:
        '''
        self._set_data_array(array)
