from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

extensions = [
    Extension("example", sources=["example.pyx"], language="c++")
]

setup(
    ext_modules = cythonize(extensions),
)