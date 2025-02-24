cmake_minimum_required(VERSION 3.18)
set(CMAKE_CUDA_ARCHITECTURES "90")
set(CMAKE_CUDA_COMPILER /usr/local/cuda-12.4/bin/nvcc)
project(lightllm_nvshmem_kernel LANGUAGES CXX CUDA)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
# 设置 CUDA 相关的选项
set(CMAKE_CUDA_STANDARD 14)  # 设置 CUDA 标准
set(CMAKE_CUDA_COMPILER /usr/local/cuda-12.4/bin/nvcc)
set(CMAKE_CUDA_FLAGS "${CMAKE_CUDA_FLAGS} -rdc=true -gencode arch=compute_90,code=sm_90 -ccbin g++")


include_directories(/usr/include/nvshmem_12/)
include_directories(/usr/local/cuda-12.4/targets/x86_64-linux/include/)
include_directories(/usr/mpi/gcc/openmpi-4.1.5a1/include/)
link_directories(/usr/lib64/nvshmem/12/)
link_directories(/usr/local/cuda-12.4/targets/x86_64-linux/lib/)
link_directories(/usr/mpi/gcc/openmpi-4.1.5a1/lib64)


# 添加可执行目标
add_library(lightllm_nvshmem_kernel SHARED ./src/kernel.cpp)
set_target_properties(lightllm_nvshmem_kernel PROPERTIES CUDA_RESOLVE_DEVICE_SYMBOLS ON)

target_link_libraries(lightllm_nvshmem_kernel nvshmem_host nvshmem_device cudart mpi)