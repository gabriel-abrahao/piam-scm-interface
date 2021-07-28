#!/bin/bash
# This creates the conda environment in environment.yml and calls pip afterwards to install
# pymagicc from a specific GitHub branch. This should be doable in the .yml but its not 
# working at the time and that's probably not the way to go anyway.
# It also creates symlinks to all GAMS libraries in the created conda environment

newenvname='test-scm' # Hardcoded here, change if changed in environment.yml

if ! command -v conda &> /dev/null
then
    echo "conda is required but not available"
    exit
else
condabin="conda"
fi
if command -v mamba &> /dev/null
then
    echo "mamba found, using it since its much faster"
    condabin="mamba"
fi
echo ""
# Getting base environment to go to in case we have to remove $newenvname first
baseenv=$($condabin info --base)
echo ""
echo "Switching to base environment "$baseenv
source activate $baseenv

# conda update is not very realiable in this case, so remove it first
echo ""
echo "Removing an existing "$newenvname

$condabin env remove --name $newenvname

echo ""
echo "Creating new environment "$baseenv
$condabin env create -f environment.yml

echo ""
echo "Activating new environment "$newenvname
source activate $newenvname

echo ""
echo "Using pip to install pymagicc from GitHub branch "
pip install --editable=git+https://github.com/gabriel-abrahao/pymagicc@pik-compatible#egg=pymagicc

# Try to activate it
source activate $newenvname &>/dev/null
if [ $? -eq 0 ]; then
    echo ""
    echo "Conda env '$newenvname' created. Activate in your shell with:"
    echo 'source activate '$newenvname
else
    echo ""
    echo "ERROR: Conda env '$newenvname' not successfully created"
fi

# Link GDX libraries of the current GAMS setup #FIXME: There's got to be a smarter way, LD_LIBRARY_PATH is not working
ln -s $(dirname $(which gams))/*.so $CONDA_PREFIX/lib/
