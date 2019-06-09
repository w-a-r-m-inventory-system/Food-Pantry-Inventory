#!/bin/bash

# delete the pdf before rerunning the QR code printer program.

# switch to expected directory
cd /Volumes/MBPC/Dvl/Python/PythonProjects/Food-Pantry-Inventory/work

# set default file name
pdffile='qr.pdf'

# check if specified on command line
if [[ $# -eq 1 ]]; then
    pdffile=$1
fi

# if file exists, delete it
if [[ -e $pdffile ]]; then
    rm $pdffile
    echo "$pdffile deleted"
fi

# EOF
