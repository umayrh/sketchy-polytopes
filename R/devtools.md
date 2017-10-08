[devtools](https://github.com/hadley/devtools) is an R package for creating structured R packages.

## Create a package

`$ Rscript -e "devtools::create('utils')"`

You should see the following files:

* `.Rbuildignore` is a text file that lists files that shouldn't be in a bundled/compiled project
* `.gitignore` is the standard gitignore file
* `DESCRIPTION` is a text file that contains package metadata such as name, author, dependencies etc
* `NAMESPACE` is a text file that contains namespaces for scoping packaging functions
* `R` is a directory containing R scripts
* `utils.Rproj` is an R Studio project metadata file 

## Edit DESCRIPTION

See [The DESCRIPTION file](https://cran.r-project.org/doc/manuals/R-exts.html#The-DESCRIPTION-file) for guidelines. Just
remember not to give your package a name like `utils`, which would conflict with existing packages.

## Add R code

Remember all R code should go under R/ directory.

## Add and publish documentation

After commenting code to your heart's desire:

`devtools::document()`

## Check package well-formedness

`devtools::check()`

## Set up unit-testing

Install `testthat`:

`install.packages(testthat)`

Set up your package for unit testing:

`devtools::use_testthat()`

Ths creates:

* `testthat` directory where all unit tests will reside
* `testthat.R` a script that will run `R CMD check` to ensure package is well-formed

## Git pre-commit hooks

[TODO] for running unit test before commiting

## References

* [R Packages](http://r-pkgs.had.co.nz)
* [Testing](http://r-pkgs.had.co.nz/tests.html
* [Documentation](http://r-pkgs.had.co.nz/man.html))
* [Devtools Vignette](https://cran.r-project.org/web/packages/devtools/devtools.pdf)
