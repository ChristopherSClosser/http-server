"""Set up file."""
from setuptools import setup

setup(
    name='http-server',
    description='simple http server',
    author='Chris Closser, David Franklin',
    py_modules=['server', 'client'],
    install_requires=[],
    extras_require={
        'testing': ['pytest'],
        'development': ['ipython']
    },
    entry_points={
        'console_scripts': [
            'runme=name:main'
        ]
    }
)
