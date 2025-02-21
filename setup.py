from setuptools import setup, Extension
import subprocess
import os

# Build the C++ library
if subprocess.call(['cmake', '.']) != 0:
    assert False, "error cmake"
    
if subprocess.call(['make']) != 0:
    assert False, "error make"

# Define the extension module
# my_library_extension = Extension(
#     'my_library1',
#     sources=[],
#     libraries=['my_library'],
#     library_dirs=['./']
# )

setup(
    name='lightllm_nvshmem_kernel',
    version='0.1',
    ext_modules=[], #[my_library_extension],
    py_modules=['nvshmem_kernel']
)