import numpy as np
import pandas as pd
import vtk
from vtk.util import numpy_support as ns


class BaseArray(object):

    def __init__(self, array, type=None):
        self._vtk = None
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
                self.numpy_to_vtk(np_array)
        else:
            raise ValueError('Expected a Numpy array, but received a: {}'.format(type(array)))
        self._vtk.AddObserver(vtk.vtkCommand.ModifiedEvent, self._update_numpy)

    @property
    def numpy(self):
        return self._numpy

    @numpy.setter
    def numpy(self, np_array):
        if np_array.flags.contiguous:
            np_array = np.ascontiguousarray(np_array)

        self._numpy = np_array
        self.numpy_to_vtk(self._numpy)

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
                    self._update_numpy()
                    return result

                return _vtk_method_proxy
            else:
                return attr
        except AttributeError as msg:
            raise AttributeError('Object has not attribute {}'.format(msg.message))

    def __eq__(self, other):
        if isinstance(other, (np.ndarray, list)):
            return np.array_equal(self._numpy, other)
        condition = True
        if isinstance(other, BaseArray):
            condition = self._numpy.shape == other.numpy.shape
        return self.GetNumberOfComponents() == other.GetNumberOfComponents() \
               and self.GetNumberOfTuples() == other.GetNumberOfTuples() \
               and condition \
               and self.GetName() == other.GetName()

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
        return '{}: {}'.format(self.GetName(), self._numpy)

    def _convert_list_pandas_to_numpy(self, data_array):
        result = None
        if isinstance(data_array, list):
            result = np.array(data_array)
        elif isinstance(data_array, pd.DataFrame):
            result = data_array.as_matrix()
        if result and not result.flags.contiguous:
            return np.ascontiguousarray(result)
        if result:
            return result
        return data_array

    def __add__(self, other):
        cls = type(self)
        add_part = self._convert_list_pandas_to_numpy(other)
        result = cls(self._numpy + add_part)
        result.SetName(self.GetName())
        return result

    def __sub__(self, other):
        cls = type(self)
        sub_part = self._convert_list_pandas_to_numpy(other)
        result = cls(self._numpy - sub_part)
        result.SetName(self.GetName())
        return result

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

    def _set_data_array(self, np_array):
        '''
        Receives a numpy array and set it to a private attribute
        :param array: numpy array
        '''
        name = self.GetName()
        new_vtk = ns.numpy_to_vtk(np_array, array_type=self._vtk.GetDataType())
        new_vtk.SetName(name)
        self._numpy = np_array
        new_vtk._np = np_array
        self._vtk = new_vtk

    def _update_numpy(self, *args, **kwargs):
        '''
        This method is called when the any method of the vtk is called
        :return:
        '''
        self._numpy = ns.vtk_to_numpy(self._vtk)


    def copy_array(self, array):
        '''
        Set the data to the vtkDataArray
        :param array: receives a pandas DataFrame, numpy array or a list
        :return:
        '''
        self._set_data_array(array)

    def numpy_to_vtk(self, num_array):
        """
        Code adapted from official VTK Project.
        License and original code can be found here:
        https://gitlab.kitware.com/vtk/vtk/blob/master/Wrapping/Python/vtk/util/numpy_support.py

        Converts a real numpy Array to a VTK array object.

        This function only works for real arrays.
        Complex arrays are NOT handled.  It also works for multi-component
        arrays.  However, only 1, and 2 dimensional arrays are supported.
        This function is very efficient, so large arrays should not be a
        problem.

        If the second argument is set to 1, the array is deep-copied from
        from numpy. This is not as efficient as the default behavior
        (shallow copy) and uses more memory but detaches the two arrays
        such that the numpy array can be released.

        WARNING: You must maintain a reference to the passed numpy array, if
        the numpy data is gc'd and VTK will point to garbage which will in
        the best case give you a segfault.

        Parameters:

        num_array
          a 1D or 2D, real numpy array.

        """

        if not num_array.flags.contiguous:
            num_array = np.ascontiguousarray(num_array)

        shape = num_array.shape
        assert num_array.flags.contiguous, 'Only contiguous arrays are supported.'
        assert len(shape) < 3, \
            "Only arrays of dimensionality 2 or lower are allowed!"
        assert not np.issubdtype(num_array.dtype, complex), \
            "Complex numpy arrays cannot be converted to vtk arrays." \
            "Use real() or imag() to get a component of the array before" \
            " passing it to vtk."

        # Fixup shape in case its empty or scalar.
        try:
            testVar = shape[0]
        except:
            shape = (0,)

        # Find the shape and set number of components.
        if len(shape) == 1:
            self._vtk.SetNumberOfComponents(1)
        else:
            self._vtk.SetNumberOfComponents(shape[1])

        self._vtk.SetNumberOfTuples(shape[0])

        # Ravel the array appropriately.
        array_flat = np.ravel(num_array)

        # Point the VTK array to the numpy data.  The last argument (1)
        # tells the array not to deallocate.
        self._vtk.SetVoidArray(array_flat, array_flat.size, 1)
        self._vtk._numpy_reference = num_array
