
************
UML Diagrams
************


Overview
========

The following is a description of this inventory system using UML diagrams.
For more information about UML diagrams, please see
`Wikipedia article <https://en.wikipedia.org/wiki/Unified_Modeling_Language>`_,
`Unofficial Explanation <https://www.smartdraw.com/uml-diagram>`_ or
`Official UML Site <https://www.uml-diagrams.org>`_.
.

Checkin
-------

:any:`Checkin Inventory Use Case <CheckinInventoryUseCase.png>`

:any:`Checkin Inventory Sequence Diagram <CheckinSequenceDiagram>`


Checkout
--------


Sub-Sub-Section
^^^^^^^^^^^^^^^


Paragraph
"""""""""

Official list of Python heading levels

    - # with overline, for parts
    - \* with overline, for chapters
    - = for sections
    - \- for subsections
    - ^ for subsubsections
    - " for paragraphs


Blah blah *italics*  **bold**

This is a numbered list

    1. Numbered items
    #. Numbered items
    #. Period can be replaced by a dash, right paren, etc., but is required.

This is a bulleted list
    - Bulleted items
    - Bulleted items
        - sublist items

Show an indented literal text block like this:

::

    literal text
    ...

Text indented the same as the "::" marker ends the literal text

A simple sample Table

============   ========================
Cell Title     Another Cell  Title
============   ========================
contents       more contents
item 1         item 2
green          purple
============   ========================

A grid table

+---------------+--------------+--------------+
| Header Col 1  | Header 2     |   Centered   |
| Extended      |              |   Header     |
+===============+==============+==============+
| Body 1        |   Body 2     |       Body 3 |
+---------------+--------------+--------------+
| Left Just     |   Centered   |   Right Just |
+---------------+--------------+--------------+
| This entry spans these cols  | This entry   |
+---------------+--------------+              +
| Blah          | Blah         | spans rows   |
+---------------+--------------+--------------+

Link to external URL: `Apple main web site <http://www.apple.com>`_ that way.

Reference to a reference elswhere in the same document:  `Link to elsewhere`_

Blah blah

    _`Link to elsewhere`   <-- This is the target of the link above.

To reference another document use

    :doc:`title <doc name and location>`

    Must not be a space between the : and the backtick!

    Can also use :any: - it will try to do :doc:, :ref:, etc.

        If not found, will then try to find a Python object with that name
        and link to it (e.g. class name, function name, module name, etc.)

Glossary-type definition
    The definition for the term must be indented and immediately below
    the term.

    Blank lines may appear in the definition body, but must not
    come between the term and the first line of definition.

    The term defined can be referenced elsewhere by :term:,
    e.g. :Glossary-type definition:
