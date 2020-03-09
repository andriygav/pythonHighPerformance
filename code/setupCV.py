from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

extensions = [
    Extension("CrossValLinearReg", sources=["CrossValLinearReg.pyx"], language="c++",
    extra_compile_args=['-fopenmp'],
    extra_link_args=['-fopenmp'],)
]

setup(
    ext_modules = cythonize(extensions),
)