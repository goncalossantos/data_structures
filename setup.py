import os

from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="data_structures",
    version="1.0.1",
    author="Goncalo Silva Santos",
    author_email="goncalopvssantos@gmail.com",
    description=("A variaty of multipurpose data structures implemented in python"),
    license="BSD",
    keywords="python data structures list queue binary search tree graph",
    url="https://github.com/goncalossantos/data_strutures",
    packages=['data_structures', 'data_structures.trees'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)