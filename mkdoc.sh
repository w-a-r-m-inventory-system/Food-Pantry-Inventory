#!/usr/bin/env bash

usage()(
    echo 'usage: mkdir [-c] [html | latex | latexpdf]'
    echo
    echo '  -c  run make before running the (optional) final parameter'
)

# set defaults for parameters
CLEAN=False
TYPE='html'

# parse command line parameters
while getopts ":abc" opt; do
    case $opt in

        c   )   CLEAN=True ;;

        \?  )   usage
                exit 1 ;;
    esac
done

shift $((OPTIND -1))

# Check final parameter if given
if [ $# == 0 ] ; then
    TYPE='html'
elif [ $# == 1 ] ;  then
    TYPE="$1"
else
    usage
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
if [ "$CLEAN" = True ]; then
    make clean
fi
make $TYPE
popd

# echo $PYTHONPATH

# EOF
