import ctypes
import os

# 加载C++库
print(os.path.join(os.path.dirname(__file__), 'liblightllm_nvshmem_kernel.so'))
lib = ctypes.CDLL(os.path.join(os.path.dirname(__file__), 'liblightllm_nvshmem_kernel.so'))


lib.init_nvshmemx_communication_ids.argtypes = (ctypes.POINTER(ctypes.c_char),)
lib.init_nvshmemx_communication_ids.restype = None

lib.init_nvshmemx_env.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_char))
lib.init_nvshmemx_env.restype = None

lib.init_nvshmemx_mpi.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_char), ctypes.c_int)
lib.init_nvshmemx_mpi.restype = None

lib.nvshmemx_mpi_port_name.argtypes = (ctypes.POINTER(ctypes.c_char), ctypes.c_int)
lib.nvshmemx_mpi_port_name.restype = None

lib.nvshmem_alloc_int32.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
lib.nvshmem_alloc_int32.restype = ctypes.POINTER(ctypes.c_int)

lib.nvshmem_alloc_int16.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
lib.nvshmem_alloc_int16.restype = ctypes.POINTER(ctypes.c_short)

lib.nvshmem_alloc_int8.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
lib.nvshmem_alloc_int8.restype = ctypes.POINTER(ctypes.c_char)


def init_nvshmemx_communication_ids(data):
    """
    data: ctypes.c_char * 1024
    return None
    
    demo input :
    data = (ctypes.c_char * 1024)()
    """
    lib.init_nvshmemx_communication_ids(data)
    return

def init_nvshmemx_env(rank:int, global_world_size:int, init_param):
    """
    init_param: ctypes.c_char * 1024
    return None
    """
    lib.init_nvshmemx_env(rank, global_world_size, init_param)
    return

def nvshmemx_mpi_port_name(port_name, port_name_length:int):
    """
    init_port_name: ctypes.c_char * 1024
    return None
    """
    lib.nvshmemx_mpi_port_name(port_name, port_name_length)
    return

def init_nvshmemx_mpi(rank:int, global_world_size:int, port_name, port_name_length:int):
    """
    init_port_name: ctypes.c_char * 1024
    return None
    """
    return lib.init_nvshmemx_mpi(rank, global_world_size, port_name, port_name_length)

def nvshmem_alloc_int32(a, b=1, c=1, d=1, dim=1):
    """
    return ctypes.POINTER(ctypes.c_int)
    """
    
    return lib.nvshmem_alloc_int32(a, b, c, d, dim)

def nvshmem_alloc_int16(a, b=1, c=1, d=1, dim=1):
    """
    return ctypes.POINTER(ctypes.c_short)
    """
    
    return lib.nvshmem_alloc_int16(a, b, c, d, dim)
    
    
def nvshmem_alloc_int8(a, b=1, c=1, d=1, dim=1):
    """
    return ctypes.POINTER(ctypes.c_char)
    """
    
    return lib.nvshmem_alloc_int8(a, b, c, d, dim)

