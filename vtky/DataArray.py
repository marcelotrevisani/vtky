from vtky.BaseArray import BaseArray
import numpy as np

class DoubleArray(BaseArray):
    def __init__(self, array=np.array([])):
        super(DoubleArray, self).__init__(array, np.double)

class FloatArray(BaseArray):
    def __init__(self, array=np.array([])):
        super(FloatArray, self).__init__(array, np.float)

class IntArray(BaseArray):
    def __init__(self, array=np.array([])):
        super(IntArray, self).__init__(array, np.int)

class UnsignedCharArray(BaseArray):
    def __init__(self, array=np.array([])):
        super(UnsignedCharArray, self).__init__(array, np.uint8)

class IdTypeArray(BaseArray):
    def __init__(self, array=np.array([])):
        super(IdTypeArray, self).__init__(array, np.int32)

class LongArray(BaseArray):
    def __init__(self, array=np.array([])):
        super(LongArray, self).__init__(array, np.int64)

class LongArray(BaseArray):
    def __init__(self, array=np.array([])):
        super(LongArray, self).__init__(array, np.int64)

class ShortArray(BaseArray):
    def __init__(self, array=np.array([])):
        super(ShortArray, self).__init__(array, np.int16)

class UnsignedIntArray(BaseArray):
    def __init__(self, array=np.array([])):
        super(UnsignedIntArray, self).__init__(array, np.uint32)

class UnsignedLongArray(BaseArray):
    def __init__(self, array=np.array([])):
        super(UnsignedLongArray, self).__init__(array, np.uint64)

class UnsignedLongLongArray(BaseArray):
    def __init__(self, array=np.array([])):
        super(UnsignedLongLongArray, self).__init__(array, np.uint64)

class UnsignedShortArray(BaseArray):
    def __init__(self, array=np.array([])):
        super(UnsignedShortArray, self).__init__(array, np.uint16)
