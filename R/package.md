# Creating R packages

## Introduction

[devtools](https://github.com/hadley/devtools) is an R package for creating structured R packages.
[usethis](https://github.com/r-lib/usethis) has taken over many of devtool's automation function, and it's
more elegant.
[testthat](https://github.com/r-lib/testthat) allows testing R packages.
[roxygen]

## Create a package

Assuming `devtools` and `usethis` have already been installed, and available in default library paths.

### Set up skeleton package

`$ Rscript -e "usethis::create_package('rUtils')"`

You should see the following files:

* `DESCRIPTION` is a text file that contains package metadata such as name, author, dependencies etc
* `NAMESPACE` is a text file that contains namespaces for scoping packaging functions
* `.Rbuildignore` is a text file that specifies files and dirs that shouldn't appear in a bundled package
* `R` is a directory containing R scripts
* `rUtils.Rproj` is an R Studio project metadata file 

We can also set this project up for Git by adding .gitignore:

`$ Rscript -e "usethis::use_git_ignore(c('.Rproj.user','.Rhistory','.RData','packrat/lib*','packrat/src'))"`

### Edit DESCRIPTION

See [The DESCRIPTION file](https://cran.r-project.org/doc/manuals/R-exts.html#The-DESCRIPTION-file) for guidelines. Just
remember not to give your package a name like `utils`, which would conflict with existing packages.

### Add documentation

Assuming `roxygen` has been installed, you can set up Roxygen using

`$ Rscript -e "usethis::use_roxygen_md()"`

After commenting code to your heart's desire:

`$ Rscript -e "devtools::document()"`

### Check package

`devtools::check()`

### Set up testing

Install `testthat`:

`install.packages(testthat)`

Set up your package for unit testing:

`devtools::use_testthat()`

Ths creates:

* `testthat` directory where all unit tests will reside
* `testthat.R` a script that will run `R CMD check` to ensure package is well-formed

### Add code

Remember all R code should go under R/ directory.

## Git hooks

See [git-hooks](../git-hooks/README.md) for details.

## Using Gradle

If you use Gradle for build management, consider using a (Gradle R plugin)[https://github.com/umayrh/gradle-plugin-r]

## References

* [R Packages](http://r-pkgs.had.co.nz)
* [Testing](http://r-pkgs.had.co.nz/tests.html
* [Documentation](http://r-pkgs.had.co.nz/man.html))
* [R Package Primer](http://kbroman.org/pkg_primer/)
* [Devtools Vignette](https://cran.r-project.org/web/packages/devtools/devtools.pdf)
