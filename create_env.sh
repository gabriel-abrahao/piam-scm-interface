#!/bin/bash
# This creates an environment using venv
# If you want to use it interactively you need to activate it again
newenvname='venv_scm' # Hardcoded here
python3 -m venv $newenvname --clear
source $newenvname'/bin/activate'
python3 -m pip install -r requirements.txt
