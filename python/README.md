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

### TODOs

* IntelliJ might be deployment dependencies from one project into another's
site-packages. This is because the Python SDK classpath refers to a project-specific
virtual env.
  * Creating an SDK per PyGradle project right now, which is manual, annoying and redundant
* Follow up on https://github.com/linkedin/pygradle/issues/273
* Follow up on https://github.com/xolox/python-humanfriendly/issues/34 and the related
https://github.com/garbas/pypi2nix/issues/135
* Consolidate the multiple places (setup.py, requirements.txt, build.gradle) where
dependencies are declared.
  * There's seemingly a vicious loop in fixing this 
  * Resources: 
    * [Dep using foreach](https://hackernoon.com/android-how-to-add-gradle-dependencies-using-foreach-c4cbcc070458)
    * [Install sequence](https://github.com/linkedin/pygradle/issues/75)
    * [PyGradle example](https://github.com/linkedin/pygradle/blob/master/examples/example-project/build.gradle)
* Unable to build a useful pex. Some dependencies don't seem to make it in.
    ```
    Starting process 'command '/Users/umayrhassan/sketchy-polytopes/python/sparktuner/build/venv/bin/python''. 
    Working directory: /Users/umayrhassan/sketchy-polytopes/python/sparktuner 
    Command: /Users/umayrhassan/sketchy-polytopes/python/sparktuner/build/venv/bin/python 
        /Users/umayrhassan/sketchy-polytopes/python/sparktuner/build/venv/bin/pex 
        --no-pypi 
        --cache-dir 
        /Users/umayrhassan/sketchy-polytopes/python/sparktuner/build/pex-cache 
        --output-file /Users/umayrhassan/sketchy-polytopes/python/sparktuner/build/deployable/bin/sparktuner.pex 
        --repo /Users/umayrhassan/sketchy-polytopes/python/sparktuner/build/wheel-cache 
        --python-shebang /usr/bin/python importlib==1.0.4 opentuner==0.8.0 chainmap==1.0.2 SQLAlchemy==0.8.2 fn==0.2.12 monotonic==1.5 numpy==1.8.0 pysqlite==2.6.3 sparktuner==0.1.0 humanfriendly==4.17 pyreadline==2.1
    ```
    And yet:
    ```
    $ build/deployable/bin/sparktuner.pex
    >>> import humanfriendly
    >>> import SQLAlchemy
    Traceback (most recent call last):
      File "<console>", line 1, in <module>
    ImportError: No module named SQLAlchemy
    ```
