#!/bin/bash

# This setup script sets up a container-like environment for installing packages (R, in particular)
# See https://github.com/craigcitro/r-travis/blob/master/scripts/travis-tool.sh

set -ex

CRAN=${CRAN:-"https://cloud.r-project.org"}

## Service versions
NEO4J_VERSION=${NEO4J_VERSION:-"3.5.14"}

# TODO: this should really come from sparkScala/gradle.properties
SPARK_VERSION=${SPARK_VERSION:-"2.4.4"}
HADOOP_VERSION=${HADOOP_VERSION:-"2.7"}
SPARK_MIRROR="http://ftp.wayne.edu/apache/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz"

## Software versions
LEMON_VERSION=${LEMON_VERSION:-"1.3.1"}
PYTHON_VERSION="2.7.13"

## Check OS type
bootstrap() {
    if [[ "linux" == "${TRAVIS_OS_NAME}" ]]; then
      bootstrapLinux
    elif [[ "osx" == "${TRAVIS_OS_NAME}" ]]; then
      bootstrapOSX
    else
      echo "Operating System not supported: $(uname -s), ${TRAVIS_OS_NAME}"
      exit 1
    fi
}

# These bootstrapping functions should be independent and idempotent.
# Even though caching offsets some of the long setup times here,
# it might be useful to parallelize these functions using GNU Parallel.

bootstrapLinux() {
  setupSpark
  setupNeo4j
  setupR_Linux
  installLemon
}

bootstrapOSX() {
  ### YUCK! Save Python from OSX!
  setupPython
  setupSpark
  setupNeo4j
  setupR_OSX
  installLemon
}

# Install Pyenv and a specific version of Python.
# Modified from https://pythonhosted.org/CodeChat/.travis.yml.html
setupPython() {
  # virtualenv doesn't work without pyenv knowledge. venv in Python 3.3
  # doesn't provide Pip by default. So, use `pyenv-virtualenv <https://github.com/yyuu/pyenv-virtualenv/blob/master/README.md>`_.
  pyenv install "${PYTHON_VERSION}"
  # I would expect something like ``pyenv init; pyenv local $PYTHON`` or
  # ``pyenv shell $PYTHON`` would work, but ``pyenv init`` doesn't seem to
  # modify the Bash environment. ??? So, I hand-set the variables instead.
  export PYENV_VERSION="${PYTHON_VERSION}"
  export PATH="${HOME}/.pyenv/shims:${PATH}"
  pyenv virtualenv venv
  pyenv global "${PYTHON_VERSION}"
  source "${HOME}"/.pyenv/versions/"${PYTHON_VERSION}"/envs/venv/bin/activate
}

## Installs a specific version of Spark
setupSpark() {
  local SPARK_DIR_NAME=spark-${SPARK_VERSION}
  if [[ ! -d "$HOME/.cache/spark" ]]; then
    cd "$HOME"/.cache
    SPARK_DIST_NAME=${SPARK_DIR_NAME}-bin-hadoop${HADOOP_VERSION}
    rm -fr "${SPARK_DIST_NAME}".tgz*
    axel --quiet "${SPARK_MIRROR}"
    tar -xf ./"${SPARK_DIST_NAME}".tgz
    # version-independent package dir to help with caching
    mv "${SPARK_DIST_NAME}" spark
    # TODO: need a more systematic method for setting up Spark properties
    echo "spark.yarn.jars=${SPARK_HOME}/jars/*.jar" > ${SPARK_HOME}/conf/spark-defaults.conf
    cd ..
  fi
  export SPARK_HOME="$HOME/.cache/spark"
}

## Installs a specific version of Neo4j
## see https://github.com/travis-ci/travis-ci/issues/3243
setupNeo4j() {
  cd "$HOME"/.cache
  if [[ ! -d "$HOME/.cache/neo4j-community" ]]; then
    rm -fr neo4j-community*
    # axel, instead of wget, fails for unknown reason
    axel --quiet dist.neo4j.org/neo4j-community-"${NEO4J_VERSION}"-unix.tar.gz
    tar -xzf neo4j-community-"${NEO4J_VERSION}"-unix.tar.gz
    # version-independent package dir to help with caching
    mv neo4j-community-"${NEO4J_VERSION}" neo4j-community
  fi
  export NEO4J_HOME=$(pwd)/neo4j-community
  neo4j-community/bin/neo4j start
  # give Neo4J some time to start
  retry curl POST http://neo4j:neo4j@localhost:7474/user/neo4j/password -d"password=neo4j2"
  curl POST http://neo4j:neo4j2@localhost:7474/user/neo4j/password -d"password=neo4j"
  cd ..
}

## Installs r-base and make R libs writable
## TODO: move to https://docs.travis-ci.com/user/languages/r/
setupR_Linux() {
  sudo add-apt-repository "deb ${CRAN}/bin/linux/ubuntu $(lsb_release -cs)-cran35/"
  sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9

  sudo add-apt-repository -y "ppa:marutter/rrutter3.5"
  sudo add-apt-repository -y "ppa:marutter/c2d4u3.5"
  sudo add-apt-repository -y "ppa:cran/libgit2"

  retry sudo apt-get -qq update
  retry sudo apt-get -qq install -y --no-install-recommends r-base-dev r-recommended qpdf libssh2-1-dev libgit2-dev
  Rscript -e 'sessionInfo()'
}

setupR_OSX() {
  # TODO: need to pin version and be consistent with Linux install
  axel --quiet "${CRAN}"/bin/macosx/R-latest.pkg
  sudo installer -pkg "./R-latest.pkg" -target /
  rm -f R-latest.pkg
  Rscript -e 'sessionInfo()'
}

# Build and installs LEMON from source
installLemon() {
  if [[ ! -d "$HOME"/.cache/lemon/build ]]; then
    cd "$HOME"/.cache
    rm -fr lemon*
    axel --quiet http://lemon.cs.elte.hu/pub/sources/lemon-"${LEMON_VERSION}".tar.gz
    tar xzf lemon-"${LEMON_VERSION}".tar.gz
    # version-independent package dir to help with caching
    mv lemon-"${LEMON_VERSION}" lemon
    cd lemon && mkdir build && cd build
    cmake ..
    make
  fi
  cd "$HOME"/.cache/lemon/build
  # Need to call 'make install' each time since Lemon headers and libs under /usr/local/*
  # would be absent on a new machine.
  sudo make install
  cd "$HOME"
}

# Retry a given command
retry() {
  if "$@"; then
    return 0
  fi
  for wait_time in 5 20 30 60; do
    echo "Command failed, retrying in ${wait_time} ..."
    sleep ${wait_time}
    if "$@"; then
        return 0
    fi
  done
  echo "Failed all retries!"
  exit 1
}

bootstrap
