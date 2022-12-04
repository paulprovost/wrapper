#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--executable-name', action='store', dest='executable_name')
parser.add_argument('rest', nargs=argparse.REMAINDER)
args, wrapped_args = parser.parse_known_args()

real_filename = args.executable_name
if not real_filename:
    real_filename = parser.prog
    
wrapper_file = sys.argv[0]
if os.path.islink(wrapper_file):
    real_wrapper_file = os.path.realpath(wrapper_file)
else:
    print(f'"{wrapper_file}" is not a link. This is not how this wrapper works.')
real_dir = os.path.dirname(os.path.dirname(real_wrapper_file))
real_filename = os.path.join(real_dir, real_filename + '.py')

venv_dir = os.path.join(real_dir, 'venv')
if os.path.isdir(venv_dir):
    interpreter_path = os.path.join(venv_dir, 'bin', 'python')
    command = [interpreter_path, real_filename]
else:
    command = [real_filename]
command.extend(wrapped_args)
command.extend(args.rest)

try:
    subprocess.run(command)
except Exception as e:
    print("Failed to launch: " + str(e))
    sys.exit(-1)
