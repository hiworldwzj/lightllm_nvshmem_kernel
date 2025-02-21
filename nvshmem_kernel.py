import ctypes
import os

# 加载C++库
print(os.path.join(os.path.dirname(__file__), 'libmy_library.so'))
lib = ctypes.CDLL(os.path.join(os.path.dirname(__file__), 'libmy_library.so'))

# 定义函数原型
lib.add.argtypes = (ctypes.c_int, ctypes.c_int)
lib.add.restype = ctypes.c_int

def add(a, b):
    return lib.add(a, b)