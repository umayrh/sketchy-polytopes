#!/bin/bash

# This setup script sets up a container-like environment for installing packages (R, in particular)
# See https://github.com/craigcitro/r-travis/blob/master/scripts/travis-tool.sh

set -ex

CRAN=${CRAN:-"http://cran.rstudio.com"}
OS=$(uname -s)
NEO4J_VERSION=${NEO4J_VERSION:-"3.4.1"}

## Check OS type
bootstrap() {
    if [[ "Linux" == "${OS}" ]]; then
        bootstrapLinux
    else
        echo "Unknown OS: ${OS}"
        exit 1
    fi
}

bootstrapLinux() {
    setupNeo4j
    #setupR
    installLemon
}

## Installs a specific version of Neo4j
## see https://github.com/travis-ci/travis-ci/issues/3243
setupNeo4j() {
    if [ ! -d "$HOME/.cache/neo4j-community-${NEO4J_VERSION}" ]; then
        wget -P $HOME/.cache dist.neo4j.org/neo4j-community-${NEO4J_VERSION}-unix.tar.gz
        cd $HOME/.cache && tar -xzf neo4j-community-${NEO4J_VERSION}-unix.tar.gz
        neo4j-community-${NEO4J_VERSION}/bin/neo4j start
        sleep 10  # give Neo4J some time to start
        curl -v POST http://neo4j:neo4j@localhost:7474/user/neo4j/password -d"password=neo4j2"
        curl -v POST http://neo4j:neo4j2@localhost:7474/user/neo4j/password -d"password=neo4j"
    fi
}

## Installs r-base and make R libs writable
## TODO: move to https://docs.travis-ci.com/user/languages/r/
setupR() {
    sudo add-apt-repository "deb ${CRAN}/bin/linux/ubuntu $(lsb_release -cs)/"
    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E084DAB9

    sudo add-apt-repository -y "ppa:marutter/rrutter"
    sudo add-apt-repository -y "ppa:marutter/c2d4u"

    retry sudo apt-get update -qq

    retry sudo apt-get install -y --no-install-recommends r-base-dev r-recommended qpdf

    sudo chmod 2777 /usr/local/lib/R /usr/local/lib/R/site-library
}

# Build and installs LEMON from source
installLemon() {
    if [ ! -d "$HOME/.cache/lemon-1.3.1" ]; then
        wget -P $HOME/.cache http://lemon.cs.elte.hu/pub/sources/lemon-1.3.1.tar.gz
        cd $HOME/.cache && tar xzvf lemon-1.3.1.tar.gz
        cd lemon-1.3.1 && mkdir build && cd build
        cmake ..
        make
        sudo make install
    fi
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
