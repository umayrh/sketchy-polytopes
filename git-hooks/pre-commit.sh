#!/bin/bash

## This pre-commit hook for looks for changes in an R packages and runs devtools::test() in that package.
## TODO:
## - Use Gradle for building and testing
## - Generalize to support other languages
## - Find a safe way to unstash any stashed changed

# Redirect output to stderr.
exec 1>&2

BASE_DIR="../"

# Exlcude files with certain extensions using regex: .*\.extension$
# So, excluding directories with READMEs and documention from testing
FILES_TO_EXCLUDE=".*/README.md$|.*\.Rd$"

# Code directories to test
DIRS_TO_TEST="^R/"

# Find staged files, exclude certain files, and find parent code directories
git diff  --name-only | egrep -v $FILES_TO_EXCLUDE | egrep $DIRS_TO_TEST | awk -F/ 'BEGIN{OFS="/"} {print $1,$2}' | sort | uniq | while read FILE; do
  if [[ -d $FILE ]]; then
    echo "working on $FILE"
    # set working directory
    CURR_DIR=`pwd`
    cd $BASE_DIR/$FILE
    R --slave -e "quit(status = sum(as.data.frame(devtools::test())[, failed]"
    if [[ ! $? -eq 0 ]]; then
        echo "Tests failed in $FILE"
        exit 1
    fi
    cd $CURR_DIR
  fi
done
