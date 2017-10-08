## Perfunctory preamble

This directory contains R code, that is structured using [devtools](https://github.com/hadley/devtools), documented using
[roxygen2](https://github.com/klutometis/roxygen) with dependencies managed using [Packrat](https://rstudio.github.io/packrat/),
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
* [R-Bloggers](https://www.r-bloggers.com)

## Moreover, and finally

A brief description of projects:

### `util`

Contains various utilities for programming in R such as:
* object deletion
