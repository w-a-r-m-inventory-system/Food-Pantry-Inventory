
###########
Other Tools
###########

blah blah

Standalone Tools
================

QR Code Printing Program
------------------------

There are three ways to print sheets of labels with QR codes on them.

*   QR Code printing program with a graphical interface.
*   QR code printing program from the command line.
*   Use the menu pick from the web page.

All three ways produce a PDF file that can be sent to a printer.  The
printer can be loaded either with plain paper or with
appropriate labels.  The program produces three QR codes across by four QR
codes down.  Each label has a box number that is not already used in the
system database.

The PDF documentm when printed, will produce one or more sheets containing
the desired QR codes.
The QR codes will be formatted for 8 1/2 by 11 (letter size)
sheets of paper.  Each QR code when printed will be aproximately two inches
square with the box name printed just above it.

It is expected that the QR codes on each page will be cut out and taped to
separate boxes.  Alternatively, the QR codes can be printed on labels so
they can be applied to separate boxes.  Once a box has had a QR code taped
to it, the QR code is expected to stay with that box until the box is no
longer usable.

Each box will have a unique box number imbedded in the QR code and shown
above the label.


QR Code Printing GUI Program
++++++++++++++++++++++++++++

This program has not yet been written.  When it has, this paragraph will be 
replaced by the instructions on how to run it.

QR Code Printing CLI Pregram
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Instructions for Use
....................

1.  Determine how many QR codes you wish to print.

#.  If desired pick a desired starting box number.

    *   Note, the program will automatically skip over any box numbers
        already in use.

#.  Obtain the "URL prefix" necessary from the system adminsitrators.

#.  Choose a file name for the PDF document.

#.  Run the program from the command prompt as follows:

::

    Usage:
        QRCodePrinter.py -p=<URL_prefix> -s <nnn> -c <nnn> -o <file>
        QRCodePrinter.py -h | --help
        QRCodePrinter.py --version
    
    Options:
        -p <URL_prefix>, --prefix=<URL_prefix>   The URL prefix for the box number
        -s <nnn>, --start=<nnn>                  Starting box number to use
        -c <nnn>. --count=<nnn>                  Number of QR codes to print
        -o <file>, --output=<file>               Output file name
        -h, --help                               Show this help and quit.
        -v, --version                            Show the version of this program and quit.

For example, assuming:

*   20 boxes need QR codes
*   Starting box number is 00001
*   URL prefix is "http://localhost:8765/fpiweb/box/box"
*   PDF document is to be named "SSL Group 5.pdf"

The command line with arguments would be:

::

    QRCodePrinter -p "http://localhost:8765/fpiweb/box/box" -s 1 -c 20 -o "SSL Group 5.pdf"

If you want to be reminded of the available options, use:

::

    QRCodePrinter --help
