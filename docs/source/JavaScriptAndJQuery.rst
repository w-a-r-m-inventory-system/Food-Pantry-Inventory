**************************
JavaScript and JQuery Tips
**************************

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


