"""
Setup file
"""


from setuptools import setup
import restream


setup(
    name='restream',
    version=restream.__version__,
    description='A python library to parse strings based on tokens and grammar rules',
    url='https://github.com/mohitudupa/restream.git',
    py_modules=['restream'],
    install_requires=[],
)
