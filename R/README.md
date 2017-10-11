## Perfunctory preamble

This directory contains R code, that is structured using [devtools](https://github.com/hadley/devtools), documented using
[roxygen2](https://github.com/klutometis/roxygen), with dependencies managed using [Packrat](https://rstudio.github.io/packrat/),
and unit-tested using [testthat](https://github.com/hadley/testthat). 

## Note on creating R packages

R packages are installed in a default directory:

`$ Rscript -e '.libPaths()'`

On a Mac, e.g., this might be "/Library/Frameworks/R.framework/Versions/3.4/Resources/library"

In general, the steps for creating well-formed R packages are:

### Install devtools and roxygen2

`$ Rscript -e "install.packages('devtools', repo='http://cran.rstudio.com'); devtools::install_github('klutometis/roxygen')"`

See devtools.md in this directory for a devtools/roxygen guide.

### Install Packrat

`$ Rscript -e "install.packages('packrat', repo='http://cran.rstudio.com')"`

See packrat.md in this directory for a Packrat guide.

## References

* [Writing R Extensions](https://cran.r-project.org/doc/manuals/R-exts.html)
* [Hadley Wickham](http://hadley.nz)'s [Advanced R Programming](https://adv-r.hadley.nz)
* [The R Journal](https://journal.r-project.org)
* [Journal of Statistical Software](https://www.jstatsoft.org/index)
* [R-Bloggers](https://www.r-bloggers.com)

## Installation notes

Compiling R packages on Mac is a bit more [involved](https://github.com/Rdatatable/data.table/wiki/Installation). In short:

* Get the latest XCode from AppStore
* Install `clang`: `brew update && brew install llvm`
* Update `~/R/.Makevars` to use `clang`:
```
CC=/usr/local/opt/llvm/bin/clang -fopenmp
CXX=/usr/local/opt/llvm/bin/clang++
# -O3 should be faster than -O2 (default) level optimisation ..
CFLAGS=-g -O3 -Wall -pedantic -std=gnu99 -mtune=native -pipe
CXXFLAGS=-g -O3 -Wall -pedantic -std=c++11 -mtune=native -pipe
LDFLAGS=-L/usr/local/opt/gettext/lib -L/usr/local/opt/llvm/lib -Wl,-rpath,/usr/local/opt/llvm/lib
CPPFLAGS=-I/usr/local/opt/gettext/include -I/usr/local/opt/llvm/include
```

## TODO

* [Linting](https://github.com/jimhester/lintr)
* [Test coverage](https://github.com/r-lib/covr)

## Moreover, and finally

A brief description of projects:

### `rUtils`

Contains various utilities for programming in R such as:
* data.table deletion

