#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--executable-name', action='store', dest='executable_name')
parser.add_argument('rest', nargs=argparse.REMAINDER)
args, wrapped_args = parser.parse_known_args()

##,-------------------------------------------------------------------
##| If an executable name was given as a parameter, use that. This is
##| mainly for using through platypus, in which case the link to
##| wrapper is called "script". If no parameter was given, fallback to
##| the invoking script's name.
##`-------------------------------------------------------------------
real_filename = args.executable_name
if not real_filename:
    real_filename = parser.prog

##,------------------------------------------------------------------
##| Get the path to the calling script and verify that is it a link.
##| If it is not, then print a warning and exit. This is not the
##| intended use.
##`------------------------------------------------------------------
wrapper_file = sys.argv[0]
if os.path.islink(wrapper_file):
    real_wrapper_file = os.path.realpath(wrapper_file)
else:
    print(f'"{wrapper_file}" is not a link. This is not how this wrapper works.')
    sys.exit(-1)

##,-------------------------------------------------------------------
##| Compute the path to the real script (one level up from the wrapper
##| script, maybe with a .py extension).
##`-------------------------------------------------------------------
real_dir = os.path.dirname(os.path.dirname(real_wrapper_file))
real_filename = os.path.join(real_dir, real_filename + '.py')
if os.path.exists(real_filename):
    ##,-----------------------------------------------------------
    ##| Python script. Check for virtual environment and build the
    ##| command to execute.
    ##`-----------------------------------------------------------
    venv_dir = os.path.join(real_dir, 'venv')
    if os.path.isdir(venv_dir):
        interpreter_path = os.path.join(venv_dir, 'bin', 'python')
        command = [interpreter_path, real_filename]
    else:
        command = [real_filename]
else:
    ##,------------------------------
    ##| Check for simple executable.
    ##`------------------------------
    real_filename = os.path.join(real_dir, real_filename)
    if not os.path.exists(real_filename):
        print(f'No executable named "{real_filename}" found')
        sys.exit(-1)
    command = [real_filename]

##,----------------------------------------------------------------
##| Add in the arguments passed to the wrapper when called from the
##| link to this script.
##`----------------------------------------------------------------
command.extend(wrapped_args)
command.extend(args.rest)

##,--------------------------
##| Run the wrapped command.
##`--------------------------
try:
    subprocess.run(command)
except Exception as e:
    print("Failed to launch: " + str(e))
    sys.exit(-1)
