from setuptools import setup
import subprocess
import os
import os.path as osp
import warnings

from torch.utils.cpp_extension import BuildExtension, CUDAExtension

ROOT_DIR = osp.dirname(osp.abspath(__file__))

__version__ = "0.0.1"

include_dirs = [osp.join(ROOT_DIR, "hashmap/include")]

CC_FLAGS = ["-std=c++17", "-Wunused-local-typedefs"]
NVCC_FLAGS = ["-std=c++17"]

CC_FLAGS += ["-O3", "-fPIC"]
NVCC_FLAGS += ["-O3", "-Xcompiler=-fno-gnu-unique,-fPIC"]

cmake_flags = [
    "-DCMAKE_POSITION_INDEPENDENT_CODE=ON",
]

# From PyTorch3D
cub_home = os.environ.get("CUB_HOME", None)
if cub_home is None:
    prefix = os.environ.get("CONDA_PREFIX", None)
    if prefix is not None and os.path.isdir(prefix + "/include/cub"):
        cub_home = prefix + "/include"

if cub_home is None:
    warnings.warn(
        "The environment variable `CUB_HOME` was not found."
        "Installation will fail if your system CUDA toolkit version is less than 11."
        "NVIDIA CUB can be downloaded "
        "from `https://github.com/NVIDIA/cub/releases`. You can unpack "
        "it to a location of your choice and set the environment variable "
        "`CUB_HOME` to the folder containing the `CMakeListst.txt` file."
    )
else:
    include_dirs.append(os.path.realpath(cub_home).replace("\\ ", " "))

try:
    ext_modules = [
        CUDAExtension(
            "__hashmap",
            [
                "hashmap/src/binding.cpp",
                "hashmap/src/hashmap.cu"
            ],
            include_dirs=include_dirs,
            # library_dirs=library_dirs,
            # libraries=libraries,
            extra_compile_args={
                "cxx": CC_FLAGS,
                "nvcc": NVCC_FLAGS,
            },
            optional=False,
        ),
    ]
except:
    import warnings

    warnings.warn("Failed to build CUDA extension")
    ext_modules = []

# shutil.copy(osp.join(library_dirs[0], 'libstdgpu.so'),
#             osp.join('/home', 'wei', 'libstdgpu.so'))

setup(
    name="hashmap",
    version=__version__,
    # author="Wei Dong",
    # author_email="weidong@andrew.cmu.edu",
    description="",
    long_description="",
    ext_modules=ext_modules,
    setup_requires=["pybind11>=2.5.0"],
    packages=["hashmap"],  # Directory name
    cmdclass={"build_ext": BuildExtension},
    zip_safe=False,
)
