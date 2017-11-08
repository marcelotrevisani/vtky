import numpy as np
import vtk

from vtky.BaseArray import BaseArray


class DoubleArray(BaseArray):
    def __init__(self, array=np.array([])):
        super(DoubleArray, self).__init__(array, vtk.VTK_DOUBLE)

class FloatArray(BaseArray):
    def __init__(self, array=np.array([])):
        super(FloatArray, self).__init__(array, vtk.VTK_FLOAT)

class IntArray(BaseArray):
    def __init__(self, array=np.array([])):
        super(IntArray, self).__init__(array, vtk.VTK_INT)

class UnsignedCharArray(BaseArray):
    def __init__(self, array=np.array([])):
        super(UnsignedCharArray, self).__init__(array, vtk.VTK_UNSIGNED_CHAR)

class IdTypeArray(BaseArray):
    def __init__(self, array=np.array([])):
        super(IdTypeArray, self).__init__(array, vtk.VTK_ID_TYPE)

class LongArray(BaseArray):
    def __init__(self, array=np.array([])):
        super(LongArray, self).__init__(array, vtk.VTK_LONG)

class LongLongArray(BaseArray):
    def __init__(self, array=np.array([])):
        super(LongLongArray, self).__init__(array, vtk.VTK_LONG_LONG)

class ShortArray(BaseArray):
    def __init__(self, array=np.array([])):
        super(ShortArray, self).__init__(array, vtk.VTK_SHORT)

class UnsignedIntArray(BaseArray):
    def __init__(self, array=np.array([])):
        super(UnsignedIntArray, self).__init__(array, vtk.VTK_UNSIGNED_INT)

class UnsignedLongArray(BaseArray):
    def __init__(self, array=np.array([])):
        super(UnsignedLongArray, self).__init__(array, vtk.VTK_UNSIGNED_LONG)

class UnsignedLongLongArray(BaseArray):
    def __init__(self, array=np.array([])):
        super(UnsignedLongLongArray, self).__init__(array, vtk.VTK_UNSIGNED_LONG_LONG)

class UnsignedShortArray(BaseArray):
    def __init__(self, array=np.array([])):
        super(UnsignedShortArray, self).__init__(array, vtk.VTK_UNSIGNED_SHORT)
