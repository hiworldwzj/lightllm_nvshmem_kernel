import ctypes
import os

# 加载C++库
print(os.path.join(os.path.dirname(__file__), 'liblightllm_nvshmem_kernel.so'))
lib = ctypes.CDLL(os.path.join(os.path.dirname(__file__), 'liblightllm_nvshmem_kernel.so'))

# 定义函数原型
lib.add.argtypes = (ctypes.c_int, ctypes.c_int)
lib.add.restype = ctypes.c_int

def add(a, b):
    return lib.add(a, b)


lib.init_nvshmemx_communication_ids.argtypes = (ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_int))
lib.init_nvshmemx_communication_ids.restype = None

lib.init_nvshmemx_env.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_int))
lib.init_nvshmemx_env.restype = None

data = (ctypes.c_char * 1024)()
length = ctypes.c_int()

if not os.path.exists("./key.txt"):
    rank = 0
    world = 2
    lib.init_nvshmemx_communication_ids(data, ctypes.byref(length))
    print(bytes(data), length)
    with open("./key.txt", mode="wb") as file:
        file.write(data[0:length.value])
    
    lib.init_nvshmemx_env(0, 2, data, ctypes.byref(length))
else:
    with open("./key.txt", mode="rb") as file:
        init_id_datas = file.read()
    for i in range(len(init_id_datas)):
        data[i] = init_id_datas[i]
    lib.init_nvshmemx_env(1, 2, data, ctypes.byref(length))

print(bytes(data), length)