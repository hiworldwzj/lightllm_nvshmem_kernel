cmake_minimum_required(VERSION 3.10)
project(lightllm_nvshmem_kernel)

set(CMAKE_CXX_STANDARD 11)

# # 查找Python模块
# find_package(PythonLibs REQUIRED)

# include_directories(${PYTHON_INCLUDE_DIRS})
# link_directories(${PYTHON_LIBRARIES})
include_directories(./src/)

# 添加库
add_library(my_library SHARED src/my_library.cpp)

# 将库与Python链接
# set_target_properties(my_library PROPERTIES PREFIX "lib")
# set_target_properties(my_library PROPERTIES SUFFIX ".so")