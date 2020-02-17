##########################
JavaScript and JQuery Tips
##########################

**************************
JavaScript Library Sources
**************************

**************************
JavaScript Library Sources
**************************

jQuery
======

Bootstrap4 apparently wants a specific version of jQuery:

    jquery-3.3.1.min.js

It can be downloaded from the `jQuery site <https://code.jquery.com/jquery/>`_
(as of Feb 2020).  Copy the file into the appropriate project directory.
Currently that is: ::

    ./Food-Project-Inventory/fpiweb/static/fpiweb/


Popper
======

Bootstrap also wants to use a library called popper.  The developers of this
library strongly urge that it be downloaded and maintained using a version
control system such as npm.  The following are suggested steps for obtaining
a current version of popper:

1.  Install npm (or pnpm).  Currently is is available via Homebrew.  (See
`Pnpm site <https://github.com/pnpm/pnpm>`_ for other ways to obtain pnpm.)

    brew install pnpm

#.  If you already have a js repository go there.  Otherwise move to an
empty directory.  Run this command to download and build popper. ::

    pnpm install @popperjs/core

#.  Go to the directory where the one file we need is
located. ::

    cd ./node_modules/@popperjs/core/dist/umd/

#.  Copy the file "popper.min.js" into the appropriate project directory.
Currently that is: ::

    ./Food-Project-Inventory/fpiweb/static/fpiweb/


The Three Levels of DOM Manipulation
====================================
There are 3 levels on which the page's Document Object Model (DOM) may be
manipulated.

1. Low-Level DOM manipulation
-----------------------------
.. code:: javascript

    // Add a paragraph with text to a div
    let div = document.getElementById('myDiv');
    let p = document.createElement('p');
    div.appendChild(p);
    let text = document.createTextNode("Hello World");
    p.appendChild(text);

    // Search through children of div element (Only 1 level down in tree)
    for(var i


2. Element-specific properties and methods
------------------------------------------
.. code:: javascript

    let field = document.getElementById('name');
    field.value = "John";


3. JQuery manipulations
-----------------------
.. code:: javascript

    let allDivs = $('div');
    allDivs.append('<p>hello</p>');


