from distutils.core import setup

setup(
    name='evolvingdag',
    version='0.1.0',
    author='Umayr Hassan',
    author_email='umayrh@gmail.com',
    packages=['src', 'test'],
    scripts=['bin/data_pipeline.py'],
    url='https://github.com/umayrh/sketchy-polytopes/tree/master/python/evolvingdag',
    license='GPL-3.0',
    description='Create and analyze random, longitudinal directed acyclic graphs',
    long_description=open('README.txt').read(),
    install_requires=[
        "networkx>=2.1"
    ],
)
