# Python projects

## Intro

This setup requires that each Python package specify
a requirements.txt file that can be used with `pip`. It should suffice to run:

`./gradlew build`

To create a new project:

* `cp -R _template new_project`
* `cd new_project && gradle generateSetupPy`
* `nano new_project/setup.py` and update project description e.g.
```
setup(
    distclass=GradleDistribution,
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,

    name='sparktuner',
    version='0.1.0',
    author='Umayr Hassan',
    author_email='umayrh@gmail.com',
    url='https://github.com/umayrh/sketchy-polytopes/tree/master/python/sparktuner',
    license='GPL-3.0',
    description='OpenTuner wrapper for tuning Spark applications',
    long_description=open('README.txt').read(),
    install_requires=[
    ]
)
```
* `gradle build` to install basic dependencies
* If using IntelliJ, ensure that the module has a Python SDK
* `pandoc --from=markdown --to=rst --output=README.txt README.md` to convert from Markdown

For more information, see PyGradle [Example Project](https://github.com/linkedin/pygradle/tree/master/examples/example-project).

## Python

* [Python Docs](https://docs.python.org/2.7/contents.html)

### Testing, style, documentation

* [PyTest](https://docs.pytest.org/en/latest/goodpractices.html#test-discovery)
* [YAPF](https://github.com/google/yapf)
* [Sphinx-Napolean](http://sphinxcontrib-napoleon.readthedocs.io/en/latest/index.html)

### Building

* [PyGradle](https://github.com/linkedin/pygradle)
  * [Prez](https://www.slideshare.net/StephenHolsapple/pythongradle-57668227)
  * [pivy-importer](https://github.com/linkedin/pygradle/blob/master/docs/pivy-importer.md) 
* [Dependencies](https://necromuralist.github.io/posts/pip-tools-and-pipdeptree/)

### Packaging

* PyPi
  * [Packaging a python library](https://blog.ionelmc.ro/2014/05/25/python-packaging/)
  * [Python Packaging](http://python-packaging.readthedocs.io/en/latest/index.html)
  * [Guide to Packaging](http://the-hitchhikers-guide-to-packaging.readthedocs.io/en/latest/index.html)
  * [Packing projects](https://packaging.python.org/tutorials/packaging-projects/)
  * [How to publish to PyPi](https://blog.jetbrains.com/pycharm/2017/05/how-to-publish-your-package-on-pypi/)
* Pex
  * [Simple Pex](https://idle.run/simple-pex)
  