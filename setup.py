"""Set up file."""
from setuptools import setup

setup(
    name='http-server',
    package_dir={'': 'src'},
    description='simple http server',
    author='Chris Closser, David Franklin',
    py_modules=['server', 'client'],
    install_requires=['gevent'],
    extras_require={
        'testing': ['pytest'],
        'development': ['ipython']
    },
)
