from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import find_packages
from setuptools import setup

setup(
    name='evolvingdag',
    version='0.1.0',
    author='Umayr Hassan',
    author_email='umayrh@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    url='https://github.com/umayrh/sketchy-polytopes/tree/master/python/evolvingdag',
    license='GPL-3.0',
    description='Create and analyze random, longitudinal directed acyclic graphs',
    long_description=open('README.txt').read(),
    install_requires=[
        "networkx>=2.2",
        "numpy>=1.14.5",
        "neo4j-driver>=1.6.0"
    ]
)
