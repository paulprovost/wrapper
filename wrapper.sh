#!/bin/sh

# readlink is different on macOS...
unamestr=`uname`
if [ "$unamestr" = 'Linux' ]; then
    readlink='readlink'
elif [ "$unamestr" = 'Darwin' ]; then
    if [ -d /opt/homebrew ]; then
        PATH=/opt/homebrew/bin:/opt/homebrew/sbin:$PATH
    else
        PATH=/usr/local/bin:/usr/local/sbin:$PATH        
    fi
    readlink=$(command -v greadlink)
    if [ $? -ne 0 ]; then
        echo "On macOS and 'greadlink' was not found. Install it using 'brew install coreutils'"
        exit 1
    fi
fi

# If the executable is a symlink, get the target and change directory to the enclosing one.
REALFILE=$(${readlink} -f -- "${0}")
REALDIR=${REALFILE%/*}

if [ ! -f ${REALDIR}/venv/bin/python ]; then
    echo "No python virtual environment found in '${REALDIR}'"
    exit 1
fi

exec ${REALDIR}/venv/bin/python "${REALFILE}".py $*
