# Installation Notes

## Mac

Assuming `brew` is installed:

To install GLPK:

* `brew install glpk`

As of 2018-02-03, this installs GLPK 4.64 along with GMP 6.1.2_1.

To install GraphViz:

* `brew install graphviz`

On Mac, headers should be under `/usr/local/include/` and libraries under `/usr/local/lib/`.

## Linux

To install GLPK from a deb:

* `sudo apt-get install glpk`

See [GLPK/Linux packages](https://en.wikibooks.org/wiki/GLPK/Linux_OS#Install).

To build GLPK from scratch, see [GLPK/Linux OS](https://en.wikibooks.org/wiki/GLPK/Linux_OS#Install).

To install GraphViz:

* `sudo apt-get install graphviz`

On Linux, headers should be under `/usr/include/` and libraries under `/usr/lib/x86_64-linux-gnu/`.
