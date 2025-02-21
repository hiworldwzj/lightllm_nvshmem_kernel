from ctypes import *

# 加载共享库
# lib = CDLL('./example.so')  # 根据实际文件名调整

# # 定义 C 函数的参数类型
# lib.process_data.argtypes = (POINTER(c_ubyte), c_int)

# 创建 bytearray
data = bytearray([1, 2, 3, 4, 5])
length = len(data)

# 将 bytearray 转换为 ctypes 类型

data_pointer = (c_ubyte * length)(*data)
print(type(data_pointer))

data_pointer[0] = 20

# 调用 C 函数
# lib.process_data(data_pointer, length)

# 获取处理后的结果
result = bytearray(data_pointer)

print(result)  # 输出处理后的数据

print(data)