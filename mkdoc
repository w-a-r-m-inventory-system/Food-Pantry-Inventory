#!/usr/bin/env bash

# Check if one parameter or none
if [ $# == 0 ] ; then
    TYPE='html'
elif [ $# == 1 ] ;  then
    TYPE="$1"
else
    echo 'usage: mkdir html | latex | latexpdf'
    exit 1
fi

# add root directory to PYTHONPATH so Sphinx will find all the modules
export PYTHONPATH=`pwd`:$PTHONPATH

# generate module stubs
sphinx-apidoc -f -M -o docs/source --tocfile FPIDjango.modules FPIDjango
sphinx-apidoc -f -M -o docs/source --tocfile fpiweb.modules fpiweb
sphinx-apidoc -f -M -o docs/source --tocfile StandaloneTools.modules StandaloneTools

# bash script to run the new Sphinx build
pushd .
cd docs
make $TYPE
popd

# echo $PYTHONPATH

# EOF
