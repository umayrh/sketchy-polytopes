#!/bin/bash

# This setup script sets up a container-like environment for installing packages (R, in particular)
# See https://github.com/craigcitro/r-travis/blob/master/scripts/travis-tool.sh

set -ex

OS=$(uname -s)

## Check OS type
bootstrap() {
    if [[ "Linux" == "${OS}" ]]; then
        bootstrapLinux
    else
        echo "Unknown OS: ${OS}"
        exit 1
    fi
}

## Installs r-base and make R libs writable
bootstrapLinux() {
    sudo add-apt-repository "deb ${CRAN}/bin/linux/ubuntu $(lsb_release -cs)/"
    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E084DAB9

    sudo add-apt-repository -y "ppa:marutter/rrutter"
    sudo add-apt-repository -y "ppa:marutter/c2d4u"

    retry sudo apt-get update -qq

    retry sudo apt-get install -y --no-install-recommends r-base-dev r-recommended qpdf

    sudo chmod 2777 /usr/local/lib/R /usr/local/lib/R/site-library
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
