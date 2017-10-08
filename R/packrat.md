[Packrat](https://rstudio.github.io/packrat/walkthrough.html) is package management software for R. 
Each packratted R package maintains a list of dependencies, along with version and source information, which
allow Packrat to download and install dependencies. Packages may be installed from CRAN, Githib, or a local 
source. Packrat expects the user to help it maintain complete transitive dependencies by installing and 
snapshotting them.

Here are some common Packrat workflows (run from within R inside the `rUtils` directory):

## Initialize ("Packrat") a package

`packrat::init(".")`

Here's sample output:

``
> packrat::init(".")
Initializing packrat project in directory:
- "~/sketchy-polytopes/R/rUtils"

Adding these packages to packrat:
            _        
    packrat   0.4.8-1

Fetching sources for packrat (0.4.8-1) ... OK (CRAN current)
Snapshot written to '/Users/umayrhassan/sketchy-polytopes/R/rUtils/packrat/packrat.lock'
Installing packrat (0.4.8-1) ... 
	OK (downloaded binary)
Initialization complete!
Packrat mode on. Using library in directory:
- "~/sketchy-polytopes/R/rUtils/packrat/lib"
```

Here's a list of all the new files in the `rUtils` directory:

* `lib`, `lib-R`, and `lib-ext` directories contain all compiled package dependencies.
* `src` directory contains all source code for package dependencies.
* `packrat.lock` is a text file that records all transitive package dependencies.
* `packrat.opts` is a text file records Packrat options for this package.
* `init.R` is a boot-strapping R script.

Henceforth, I expect to see the following log when running R inside `rUtils`:

```
Packrat mode on. Using library in directory:
- "~/sketchy-polytopes/R/rUtils/packrat/lib"
```

## Adding a dependency

To use `pryr` in `rUtils`, I first install it (and, implicitly, all of `pryr`'s dependencies)

`install.packages("pryr")`

and then "snapshot" it (and, implicitly, all of `pryr`'s dependencies).

`packrat::snapshot()`

```
Installing package into ‘~/sketchy-polytopes/R/rUtils/packrat/lib/.../3.4.2’
(as ‘lib’ is unspecified)
also installing the dependencies ‘stringi’, ‘magrittr’, ‘stringr’, ‘Rcpp’`
...
Snapshot written to '~/sketchy-polytopes/R/rUtils/packrat/packrat.lock'
```

Installing a local package, however, first requires setting the local.repo option in packrat.opt.

`packrat::set_opts(local.repos = "~/sketchy-polytopes/R")`

## Packrat and devtools

Unfortunately, Packrat doesn't play with devtools. So e.g. you may need to specify dependencies in 
your package's DESCRIPTION file. After packratting a project, you may have to download `devtools`
and `roxygen` (again!) to put them in Packrat's private library.

## References

[Packrat Guide](https://rstudio.github.io/packrat/walkthrough.html)
[Packrat Github](https://github.com/rstudio/packrat)
[R-Bloggers](https://www.r-bloggers.com/creating-reproducible-software-environments-with-packrat/)
