#!/bin/sh

##,-----------------------------------
##| readlink is different on macOS...
##`-----------------------------------
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

##,--------------
##| parse options
##`--------------
while getopts ":n:" opt; do
  case $opt in
    n) REAL_FILENAME="$OPTARG" ; shift 2 ;;
  esac
done

##,----------------------------------------------------------
##| If the executable is a symlink, get the target and change
##| directory to the enclosing one.
##`----------------------------------------------------------
if [ -z "$REAL_FILENAME" ]; then
    REAL_FILENAME="${0##*/}"
fi
REAL_WRAPPER_FILE=$(${readlink} -f -- "${0}")
REAL_WRAPPER_DIR=${REAL_WRAPPER_FILE%/*}
REAL_DIR=${REAL_WRAPPER_DIR%/*}

if [ ! -f ${REAL_DIR}/venv/bin/python ]; then
    exec "${REAL_DIR}/${REAL_FILENAME}".py $*
    exit 1
fi

exec ${REAL_DIR}/venv/bin/python "${REAL_DIR}/${REAL_FILENAME}".py "$*"
