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

TODO: how does 

## Add R code

Remember all R code should go under R/ directory.

## Add and publish documentation

After commenting your code to you heart's desire:

`devtools::document()`

## Check package well-formedness

`devtools::check()`

## References

[R Packages](http://r-pkgs.had.co.nz)
[Vignette](https://cran.r-project.org/web/packages/devtools/devtools.pdf)
[Hilary Parker](https://hilaryparker.com/2014/04/29/writing-an-r-package-from-scratch/)
